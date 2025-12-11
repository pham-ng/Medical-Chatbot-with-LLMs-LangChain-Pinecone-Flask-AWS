from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from tqdm import tqdm  # Thư viện tạo thanh tiến trình
import time

# Import từ helper của bạn
from src.helper import load_and_split_pdfs, download_embeddings, pc, INDEX_NAME, PINECONE_API_KEY

def create_and_ingest():
    print("🚀 [Store Index] Bắt đầu quy trình ETL...")
    
    # --- 1. Load & Split Data ---
    text_chunks = load_and_split_pdfs("data")
    if not text_chunks:
        print("❌ Không có dữ liệu để nạp. Hãy kiểm tra folder 'data'.")
        return

    # --- 2. Embedding ---
    embeddings = download_embeddings()

    # --- 3. Tạo Index nếu chưa có ---
    # Lấy danh sách index hiện tại
    existing_indexes = [index["name"] for index in pc.list_indexes()]
    
    if INDEX_NAME not in existing_indexes:
        print(f"📦 Index '{INDEX_NAME}' chưa có. Đang tạo mới...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=768,  # Dimension của model intfloat/multilingual-e5-base
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        # Chờ một chút để Index khởi tạo xong trên Cloud
        print("⏳ Đang chờ Pinecone khởi tạo Index...")
        time.sleep(10) 
    else:
        print(f"ℹ️ Index '{INDEX_NAME}' đã tồn tại. Sẽ nạp thêm dữ liệu vào.")

    # --- 4. Upload với thanh tiến trình (TQDM) ---
    print(f"⬆️ Chuẩn bị upload {len(text_chunks)} vectors lên Pinecone...")
    
    # Bước A: Khởi tạo kết nối tới Vector Store (Chưa upload gì cả)
    vector_store = PineconeVectorStore(
        index_name=INDEX_NAME,
        embedding=embeddings,
        pinecone_api_key=PINECONE_API_KEY
    )
    
    # Bước B: Chia nhỏ và upload từng batch
    batch_size = 100  # Upload 100 chunk mỗi lần (an toàn và nhanh)
    
    # Vòng lặp có thanh loading
    for i in tqdm(range(0, len(text_chunks), batch_size), desc="Đang tải lên"):
        # Cắt lấy 100 phần tử
        batch = text_chunks[i : i + batch_size]
        
        # Đẩy lên Pinecone
        vector_store.add_documents(
            documents=batch
        )
        
    print("\n✅ NẠP DỮ LIỆU THÀNH CÔNG! Dữ liệu đã sẵn sàng trên Pinecone.")

if __name__ == "__main__":
    create_and_ingest()