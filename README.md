# Medical-Chatbot-with-LLMs-LangChain-Pinecone-Flask-AWS
# 🏥 BachMai-MedicalBot: Trợ lý AI Tư vấn Y tế & Sức khỏe

![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker)
![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20ECR-FF9900?style=for-the-badge&logo=amazon-aws)

**Hệ thống RAG (Retrieval-Augmented Generation) chuyên sâu lĩnh vực y tế, hỗ trợ tra cứu bệnh lý và thuốc dựa trên tài liệu chuẩn.**

---

## 📖 Giới thiệu

 **BachMai-MedicalBot** ra đời nhằm cung cấp một công cụ tra cứu tin cậy,hoạt động dựa trên cơ chế tìm kiếm và trích xuất thông tin từ các tài liệu PDF y khoa chính thống. Dự án được xây dựng với mục đích học tập và nghiên cứu ứng dụng AI trong Y tế, không nhằm mục đích thương mại.

Dự án được triển khai tự động hóa hoàn toàn (CI/CD) trên nền tảng **AWS Cloud**, đảm bảo tính sẵn sàng và khả năng mở rộng cao.



📂 Cấu trúc thư mục (Project Structure)
Plaintext

Medical-Chatbot/

├── .github/workflows/    
├── data/                 
├── src/                 
│   ├── helper.py         
│   ├── prompt.py         
│   └── database.py       
├── templates/            
├── static/               
├── app.py                
├── Dockerfile            
└── README.md             



## ✨ Tính năng nổi bật (Key Features)

- 🩺 **Tư vấn y khoa chính xác:** Trả lời dựa trên ngữ cảnh được trích xuất từ sách y học (Evidence-based).
- 🧠 **Bộ nhớ ngữ cảnh (Contextual Memory):** Hệ thống ghi nhớ lịch sử chat (sử dụng SQLite), cho phép hỏi đáp nối tiếp tự nhiên.
- 🔍 **Tìm kiếm lai (Hybrid Search):** Kết hợp Vector Search (Pinecone) và Re-ranking (Cohere) để tối ưu độ chính xác của tài liệu tìm được.
- ⚙️ **DevOps Automation:** Tích hợp quy trình CI/CD với GitHub Actions, Docker và AWS ECR/EC2.

## 🏗️ Kiến trúc hệ thống (System Architecture)

Hệ thống hoạt động theo luồng RAG Pipeline tiêu chuẩn:

<img width="1067" height="448" alt="image" src="https://github.com/user-attachments/assets/b24e7393-68c3-4892-9474-f41a66997eb6" />

## 📚 Bộ Dữ Liệu & Quy Trình Xử Lý (Dataset & ETL)

### 1. Nguồn dữ liệu (Data Sources)
Hệ thống được xây dựng dựa trên nguồn tri thức y khoa uy tín, đảm bảo tính chính xác và hạn chế ảo giác (hallucination):
* **Tài liệu quốc tế:** Bộ sách *The Gale Encyclopedia of Medicine* (Tiêu chuẩn vàng về tra cứu y học).
* **Tài liệu trong nước:** Giáo trình chính quy từ **Đại học Y Hà Nội**.
* **Hướng dẫn điều trị:** Phác đồ điều trị và hướng dẫn chẩn đoán mới nhất từ **Bộ Y Tế Việt Nam**.

### 📊 Thống kê dữ liệu (Statistics)
> Hệ thống hiện tại đã xử lý và đánh chỉ mục (index) thành công:
> * **3.300+** trang tài liệu chuyên sâu.
> * **7.020** vector chunks sẵn sàng cho việc truy xuất.
  
## 🔍 Quy Trình Xử Lý & Triển Khai (Processing Pipeline)

Hệ thống vận hành dựa trên kiến trúc **RAG (Retrieval-Augmented Generation)** tiêu chuẩn, được tối ưu hóa qua 4 bước:

### 1. Chia nhỏ dữ liệu (Chunking)
* **Kỹ thuật:** Sử dụng `Recursive Character Text Splitter` của LangChain.
* **Cấu hình:** Chia văn bản thành các đoạn nhỏ khoảng **500 tokens**.
* **Mục tiêu:** Đảm bảo ngữ cảnh không bị cắt giữa chừng. Mỗi chunk được gắn metadata chi tiết (*Tên sách, Số trang, Loại bệnh*) để phục vụ trích dẫn nguồn chính xác.

### 2. Mã hóa Vector (Embedding)
* **Mô hình:** `intfloat/multilingual-e5-base` (Huggingface).
* **Đặc điểm:** Chuyển đổi văn bản sang vector **768 chiều**.
* **Ưu điểm:** Khả năng bắt ngữ nghĩa (semantic) vượt trội, giúp hệ thống hiểu được ý định người dùng ngay cả khi từ khóa không khớp hoàn toàn (khác với tìm kiếm từ khóa truyền thống).

### 3. Tìm kiếm & Sàng lọc (Hybrid Retrieval & Rerank)
Hệ thống áp dụng chiến lược **Hybrid Search** (Tìm kiếm lai) để tối ưu hóa độ chính xác:

* **Bước 1 - Truy xuất đa chiều (Hybrid Retrieval):**
    Kết hợp kết quả từ hai luồng tìm kiếm song song trên **Pinecone**:
    * **Keyword Search (BM25):** Tập trung bắt chính xác các từ khóa chuyên ngành, tên thuốc, hoặc các thuật ngữ y khoa cụ thể (Sparse Vector).
    * **Semantic Search (Dense Vector):** Tìm kiếm dựa trên sự tương đồng về ngữ nghĩa, giúp hệ thống hiểu được ý định người dùng ngay cả khi không dùng từ khóa chính xác.

* **Bước 2 - Tái xếp hạng (Re-ranking):**
    * Sử dụng mô hình **Cohere Rerank**.
    * > *Tại sao cần bước này?* Việc gộp kết quả từ Hybrid Search có thể tạo ra danh sách dài chứa cả những thông tin nhiễu. Cohere đóng vai trò "giám khảo", đọc hiểu sâu từng đoạn văn và chấm điểm lại, chỉ giữ lại những đoạn thực sự trả lời đúng câu hỏi của người dùng để gửi cho AI xử lý.
      
### 4. Sinh câu trả lời (Generation)
* **Mô hình:** `GPT-4o` (hoặc GPT-3.5 Turbo).
* **Cơ chế:**
    1.  Nhận đầu vào: *Câu hỏi + Context (đã lọc) + Lịch sử chat*.
    2.  Hệ thống áp dụng **System Prompt** nghiêm ngặt để ép mô hình chỉ trả lời dựa trên dữ liệu cung cấp.
    3.  Đưa ra câu trả lời cuối cùng kèm trích dẫn nguồn tài liệu.
# HOW TO RUN?
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
    - Save the URI: 533267408537.dkr.ecr.us-east-1.amazonaws.com/medicalbot

	
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
- AWS_ACCOUNT_ID
- AWS_DEFAULT_REGION
- AWS_SECRET_ACCESS_KEY
- COHERE_API_KEY
- EC2_HOST
- EC2_SSH_KEY
- EC2_USER
- ECR_REPO
- OPENAI_API_KEY
- PINECONE_API_ENV
- PINECONE_API_KEY
<img width="1601" height="358" alt="image" src="https://github.com/user-attachments/assets/150e118e-9e36-47bc-9222-783c5af7757c" />

## 🖥️ Giao Diện Người Dùng
Hệ thống tích hợp một giao diện đơn giản, trực quan:

- Nhập câu hỏi liên quan đến các bệnh phổ biến
- Trình bày câu trả lời được sinh từ mô hình
- Cho phép lưu lại lịch sử cuộc trò chuyện
- Upload thêm tài liệu y khoa

*(Giao diện trực quan khi hỏi đáp về triệu chứng và cách dùng thuốc)*

<img width="1893" height="862" alt="image" src="https://github.com/user-attachments/assets/30e09196-3d3d-4bdf-8aea-4f87192ebbe4" />
<img width="1894" height="863" alt="image" src="https://github.com/user-attachments/assets/c836527d-5783-44bf-b1a6-c8d59d6cec59" />
<img width="1897" height="865" alt="image" src="https://github.com/user-attachments/assets/64169647-069c-4281-8f69-8d095e2ac529" />
<img width="1915" height="849" alt="image" src="https://github.com/user-attachments/assets/5cff0d34-dfb0-47bf-951d-36f0491ffe92" />

## 🚧 Hạn Chế & Hướng Phát Triển (Future Roadmap)

Dù đã hoạt động ổn định, tôi nhận thấy **BachMai-MedicalBot** vẫn còn nhiều dư địa để cải thiện nhằm đạt độ chính xác cấp độ lâm sàng. Dưới đây là lộ trình phát triển sắp tới:

### 1. Nâng cấp chất lượng dữ liệu (Data Quality)
* **Hiện tại:** Dữ liệu chủ yếu từ sách giáo khoa chung.
* **Tương lai:** Tích hợp **Knowledge Graph (Đồ thị tri thức)** để mô hình hiểu sâu hơn mối quan hệ phức tạp giữa *Triệu chứng - Bệnh lý - Thuốc*, thay vì chỉ tìm kiếm văn bản thuần túy. Bổ sung nguồn dữ liệu từ PubMed và hướng dẫn điều trị mới nhất của Bộ Y tế.

### 2. Tối ưu kỹ thuật Chunking (Advanced Chunking)
* **Hiện tại:** Recursive Character Splitter (Cắt theo ký tự).
* **Tương lai:** Áp dụng **Semantic Chunking** (Cắt theo ngữ nghĩa) hoặc **Parent-Child Chunking** (Truy xuất đoạn nhỏ nhưng đưa vào ngữ cảnh lớn) để AI không bị mất thông tin khi đoạn văn bị cắt giữa chừng.

### 3. Cải thiện bộ nhớ & Ngữ cảnh (Memory & Context)
* **Hiện tại:** Lưu lịch sử chat cơ bản (Buffer Memory).
* **Tương lai:** Triển khai **Summary Buffer Memory** (Tóm tắt hội thoại cũ) để AI nhớ được các thông tin quan trọng của bệnh nhân (tuổi, tiền sử bệnh) trong suốt quá trình tư vấn dài mà không bị giới hạn token.

### 4. Đánh giá chuyên sâu (Evaluation)
* Xây dựng bộ test **RAGAS (RAG Assessment)** để tự động chấm điểm độ chính xác (Faithfulness) và độ liên quan (Relevance) của câu trả lời, thay vì chỉ đánh giá cảm tính.

---

## ❤️ Lời Kết & Đóng Góp

Dự án này xuất phát từ mong muốn nhỏ bé: **Dùng công nghệ để làm cho kiến thức y tế trở nên dễ tiếp cận hơn với mọi người.**

Tuy nhiên, Y tế là một lĩnh vực đặc thù đòi hỏi sự chính xác tuyệt đối. Tôi hiểu rằng mô hình hiện tại vẫn chỉ là một bản thử nghiệm (Proof of Concept) và chắc chắn còn nhiều sai sót về mặt chuyên môn.

Rất mong nhận được sự góp ý từ cộng đồng lập trình viên và các chuyên gia y tế để hoàn thiện sản phẩm này. Mọi ý tưởng đóng góp (Pull Requests) hoặc báo lỗi (Issues) đều là những món quà quý giá đối với tôi.

> *"Code có thể sửa, nhưng sức khỏe là vô giá. Hãy sử dụng Chatbot này như một kênh tham khảo, và luôn tìm đến bác sĩ chuyên khoa cho các quyết định điều trị."*

---

