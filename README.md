
# BachMai-MedicalBot 🏥🩺

**Hệ thống Tư vấn Y khoa & Hỗ trợ Chẩn đoán sơ bộ**  
Dựa trên kiến trúc **RAG (Retrieval-Augmented Generation)** hiện đại, mang phong cách phục vụ tận tâm của Bệnh viện Bạch Mai.

Dự án giúp bệnh nhân và nhân viên y tế tra cứu nhanh, chính xác các thông tin về bệnh lý, triệu chứng, phác đồ điều trị, hướng dẫn chẩn đoán và thông tin thuốc – với trích dẫn nguồn rõ ràng và phản hồi theo thời gian thực.

---

### 📚 Bộ Dữ Liệu Y Khoa (Medical Dataset)

Dữ liệu được tuyển chọn kỹ lưỡng từ các nguồn chính thống, uy tín bậc nhất tại Việt Nam:

| Loại tài liệu                              | Nguồn chính thức                                      |
|-------------------------------------------|-------------------------------------------------------|
| Sách giáo khoa Y khoa kinh điển           | Bệnh học Nội khoa (ĐH Y Hà Nội), Triệu chứng học & Điều trị học |
| Dược lý & Thông tin thuốc                  | Dược lý học, Dược thư Quốc gia Việt Nam               |
| Hướng dẫn chẩn đoán & điều trị             | Phác đồ, quyết định chính thức của Bộ Y tế Việt Nam   |

**Quy trình xử lý dữ liệu**

- Thu thập & Upload: Hỗ trợ dữ liệu tĩnh ban đầu + Dynamic Ingestion (người dùng tự upload PDF mới qua giao diện)
- Làm sạch: PyPDFLoader + PDFPlumber (loại bỏ header/footer, bảng biểu nhiễu)
- Chunking: Recursive Character Text Splitter (500 tokens/chunk, overlap 100 tokens) để giữ ngữ cảnh y khoa phức tạp

---

### 🧠 Kiến trúc Hybrid RAG + Rerank (Tối ưu cho Y khoa tiếng Việt)

| Thành phần               | Công nghệ & Mô tả                                                                                   |
|--------------------------|-----------------------------------------------------------------------------------------------------|
| **Hybrid Retriever**     | Kết hợp 40% BM25 (Keyword) + 60% Semantic Search (Pinecone)<br>→ Bắt chính xác cả tên thuốc, chỉ số xét nghiệm và ý định người dùng |
| **Reranker**             | Cohere Rerank v3.0 Multilingual – sắp xếp lại kết quả để đoạn liên quan nhất lên đầu                |

---

### ⚙️ Công nghệ & Mô hình

| Thành phần               | Công nghệ sử dụng                                          |
|--------------------------|------------------------------------------------------------|
| LLM (Generation)         | GPT-4o-mini (OpenAI) – nhanh, tiết kiệm chi phí            |
| Vector Database          | Pinecone Serverless                                        |
| Embedding Model          | `intfloat/multilingual-e5-base` (hiểu tốt tiếng Việt + Anh)|
| Reranker                 | Cohere Rerank v3.0 Multilingual                            |
| Backend                  | Python Flask + Waitress (production-ready)                 |
| Frontend                 | HTML5/CSS3 (giao diện phong cách BV Bạch Mai) + Marked.js  |
| Infrastructure           | Docker, AWS EC2, GitHub Actions (CI/CD)                    |

---

### 🔍 Quy trình hoạt động (Pipeline)

<img width="1067" height="448" alt="image" src="https://github.com/user-attachments/assets/57d37c89-43fb-4067-9ff4-98b9227f7af9" />

# How to run?
### STEPS:

Clone the respository

```bash
Project repo: https://github.com/pham-ng/Medical-Chatbot-with-LLMs-LangChain-Pinecone-Flask-AWS.git
```

### STEP 01: Create a conda environment after opening the reposiotry


```bash
conda create -n medicalbot python=3.10 -y

conda activate medicalbot
```


### STEP 02: Install the requirements

```bashs 
pip install -r requirements.txt
```




### Create a `.env` file in the root directory and add your Pinecone & openai credentials as follows:

```ini
PINECONE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
OPENAI_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
COHERE_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

```

```bash
# run the following command to store embeddings to pinecone
python store_index.py
```

```bash
# Finally run the following command
python app.py
```

Now,
```bash
open up localhost:
```


### Techstack Used:

- Python
- LangChain
- Flask
- GPT
- Pinecone
- CoheRererank
- BM25Search



# AWS-CICD-Deployment-with-Github-Actions

## 1. Login to AWS console.

## 2. Create IAM user for deployment

	#with specific access

	1. EC2 access : It is virtual machine

	2. ECR: Elastic Container registry to save your docker image in aws


	#Description: About the deployment

	1. Build docker image of the source code

	2. Push your docker image to ECR

	3. Launch Your EC2 

	4. Pull Your image from ECR in EC2

	5. Lauch your docker image in EC2

	#Policy:

	1. AmazonEC2ContainerRegistryFullAccess

	2. AmazonEC2FullAccess

	
## 3. Create ECR repo to store/save docker image
    - Save the URI: 315865595366.dkr.ecr.us-east-1.amazonaws.com/medicalbot

	
## 4. Create EC2 machine (Ubuntu) 

## 5. Open EC2 and Install docker in EC2 Machine:
	
	
	#optinal

	sudo apt-get update -y

	sudo apt-get upgrade
	
	#required

	curl -fsSL https://get.docker.com -o get-docker.sh

	sudo sh get-docker.sh

	sudo usermod -aG docker ubuntu

	newgrp docker
	
# 6. Configure EC2 as self-hosted runner:
    setting>actions>runner>new self hosted runner> choose os> then run command one by one


# 7. Setup github secrets:

   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - AWS_DEFAULT_REGION
   - ECR_REPO
   - PINECONE_API_KEY
   - OPENAI_API_KEY

### 🖥️ Giao Diện Người Dùng

Hệ thống tích hợp một giao diện đơn giản, trực quan:

- Nhập câu hỏi liên quann đến sức khỏe
- Trình bày câu trả lời được sinh từ mô hình
- Cho phép tải thêm tài liệu chuyên khoa
- Tra cứu đa ngôn ngữ: Tiếng Việt và Tiếng Anh
- Trích dẫn nguồn đầy đủ, tránh hiện tượng Hallucination 
<img width="1916" height="849" alt="image" src="https://github.com/user-attachments/assets/e65ec7c1-1b7c-4ec9-a390-b87c97fef576" />
<img width="1907" height="861" alt="image" src="https://github.com/user-attachments/assets/0943602f-1fd7-4a93-8647-411d5d4b5ca2" />
<img width="1919" height="867" alt="image" src="https://github.com/user-attachments/assets/44818749-6bb7-4ab7-8457-cbfebeb5c1bb" />

