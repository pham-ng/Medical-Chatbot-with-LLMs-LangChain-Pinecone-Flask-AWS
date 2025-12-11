import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from src.helper import medical_rag_pipeline, initialize_system, process_uploaded_file

app = Flask(__name__)

# Cấu hình upload
app.config['UPLOAD_FOLDER'] = 'data'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Giới hạn file 16MB
ALLOWED_EXTENSIONS = {'pdf'}

# Tạo thư mục data nếu chưa có
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- KHỞI TẠO HỆ THỐNG LẦN ĐẦU ---
print("⏳ Đang khởi tạo hệ thống lần đầu...")
initialize_system()
print("✅ Hệ thống đã sẵn sàng!")

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get_response", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("msg")
    if not user_input:
        return jsonify({"answer": "Vui lòng nhập câu hỏi."})
    response_text = medical_rag_pipeline(user_input)
    return jsonify({"answer": response_text})

# --- API UPLOAD FILE MỚI ---
@app.route("/upload_doc", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "Không tìm thấy file."})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"status": "error", "message": "Chưa chọn file."})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        
        # Gọi hàm xử lý trong helper
        success, msg = process_uploaded_file(save_path)
        
        if success:
            # Load lại hệ thống ngay lập tức để cập nhật BM25
            initialize_system()
            return jsonify({"status": "success", "message": msg})
        else:
            return jsonify({"status": "error", "message": msg})
    
    return jsonify({"status": "error", "message": "Chỉ chấp nhận file PDF!"})

if __name__ == '__main__':
    print("🏥 Server Bạch Mai đang chạy tại http://localhost:5001")
    app.run(host="0.0.0.0", port=5001, debug=True)