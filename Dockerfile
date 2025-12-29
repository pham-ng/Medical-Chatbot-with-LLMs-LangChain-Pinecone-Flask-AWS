# Sử dụng Python 3.9 bản gọn nhẹ
FROM python:3.10-slim-buster

# Cài đặt các thư viện hệ thống cần thiết (quan trọng cho PDFPlumber/LangChain)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy file requirements và cài đặt thư viện Python
COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt

# Lệnh chạy ứng dụng
CMD ["python", "app.py"]


