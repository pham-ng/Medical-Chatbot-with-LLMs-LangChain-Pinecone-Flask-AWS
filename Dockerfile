# Đổi từ 'slim-buster' (cũ) sang 'slim' (mới nhất, hiện là Debian Bookworm)
FROM python:3.10-slim

# 1. Cài đặt các gói hệ thống cần thiết
# Thêm --no-install-recommends để giảm nhẹ image
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpoppler-cpp-dev \
    pkg-config \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Thiết lập thư mục làm việc
WORKDIR /app

# 3. Copy requirements và cài đặt thư viện trước (Tận dụng Cache)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 4. Copy toàn bộ code vào sau
COPY . .

# 5. Mở port 5001 (Port của Flask/Waitress)
EXPOSE 5001

# 6. Lệnh chạy (Đảm bảo tên file là app.py hoặc run.py tùy code bạn)
CMD ["python", "app.py"]