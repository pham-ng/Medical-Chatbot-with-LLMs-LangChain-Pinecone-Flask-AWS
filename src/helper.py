import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, PDFPlumberLoader
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from pinecone import Pinecone
import cohere
from openai import OpenAI

try:
    from src.prompt import build_rag_prompt
except ImportError:
    from .prompt import build_rag_prompt

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")
INDEX_NAME = "medical-chatbot"

pc = Pinecone(api_key=PINECONE_API_KEY)
cohere_client = cohere.Client(COHERE_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Biến cache toàn cục
global_retriever = None 

# --- CÁC HÀM CƠ BẢN ---
def download_embeddings():
    print("   🧠 [AI] Đang tải model Embedding...")
    return HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-base", 
        model_kwargs={"device": "cpu"}
    )

def load_and_split_pdfs(data_dir: str):
    if not os.path.exists(data_dir): return []
    try:
        print(f"   📂 [Loader] Đang đọc PDF từ {data_dir}...")
        loader = DirectoryLoader(data_dir, glob="**/*.pdf", loader_cls=PDFPlumberLoader)
        documents = loader.load()
        if not documents: return []
        
        minimal_docs = [Document(page_content=d.page_content.strip(), metadata=d.metadata) for d in documents]
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        return text_splitter.split_documents(minimal_docs)
    except Exception as e:
        print(f"   ❌ Lỗi load PDF: {e}")
        return []

# --- HÀM KHỞI TẠO (CHẠY 1 LẦN) ---
def initialize_system():
    global global_retriever
    if global_retriever is not None:
        return global_retriever

    print("\n🚀 [SYSTEM] ĐANG KHỞI ĐỘNG HỆ THỐNG RAG...")
    
    # 1. BM25 (RAM)
    docs = load_and_split_pdfs("data")
    if docs:
        print("   🔍 [BM25] Đang xây dựng chỉ mục từ khóa...")
        bm25_retriever = BM25Retriever.from_documents(docs)
        bm25_retriever.k = 10
    else:
        bm25_retriever = None

    # 2. Pinecone (Cloud)
    embeddings = download_embeddings()
    print("   ☁️ [Pinecone] Đang kết nối cơ sở dữ liệu...")
    vectorstore = PineconeVectorStore.from_existing_index(index_name=INDEX_NAME, embedding=embeddings)
    pinecone_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

    # 3. Kết hợp
    if bm25_retriever:
        print("   ⚡ [Ensemble] Đang kết hợp BM25 + Vector...")
        global_retriever = EnsembleRetriever(retrievers=[bm25_retriever, pinecone_retriever], weights=[0.4, 0.6])
    else:
        global_retriever = pinecone_retriever

    print("✅ HỆ THỐNG ĐÃ SẴN SÀNG PHỤC VỤ!\n")
    return global_retriever

# --- HÀM XỬ LÝ FILE MỚI UPLOAD ---
def process_uploaded_file(filepath):
    global global_retriever
    print(f"📥 [Upload] Đang xử lý file mới: {filepath}...")
    
    # 1. Load & Split file này
    try:
        loader = PyPDFLoader(filepath)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = text_splitter.split_documents(docs)
        print(f"   ✅ Đã cắt thành {len(chunks)} chunks.")
    except Exception as e:
        return False, f"Lỗi đọc PDF: {str(e)}"

    # 2. Upload lên Pinecone
    try:
        embeddings = download_embeddings()
        print("   ☁️ Đang đẩy lên Pinecone...")
        PineconeVectorStore.from_documents(documents=chunks, index_name=INDEX_NAME, embedding=embeddings)
        print("   ✅ Upload Pinecone thành công!")
    except Exception as e:
        return False, f"Lỗi Pinecone: {str(e)}"

    # 3. Reset cache để lần sau load lại BM25
    global_retriever = None 
    print("   🔄 Đã đặt lệnh reset hệ thống.")
    return True, "Đã thêm tài liệu thành công! Bạn có thể hỏi ngay bây giờ."

# --- PIPELINE CHÍNH ---
def medical_rag_pipeline(user_query):
    if not user_query: return "Vui lòng nhập câu hỏi."
    
    # Dịch câu hỏi (Optional)
    search_query = user_query
    try:
        trans = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "Translate to English"}, {"role": "user", "content": user_query}],
            temperature=0
        )
        search_query = trans.choices[0].message.content.strip()
    except: pass

    # Lấy Retriever từ cache
    retriever = initialize_system()
    if not retriever: return "Hệ thống đang khởi động..."
    
    try:
        initial_docs = retriever.invoke(search_query)
    except: return "Lỗi tìm kiếm."

    # Rerank
    passages = [d.page_content for d in initial_docs]
    try:
        rerank = cohere_client.rerank(model="rerank-multilingual-v3.0", query=search_query, documents=passages, top_n=5)
        final_docs = [initial_docs[r.index] for r in rerank.results]
    except: final_docs = initial_docs[:5]

    # Generate
    sys_msg, user_msg = build_rag_prompt(user_query, final_docs)
    try:
        res = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": user_msg}],
            temperature=0.3
        )
        return res.choices[0].message.content
    except Exception as e: return f"Lỗi OpenAI: {e}"