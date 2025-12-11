document.addEventListener('DOMContentLoaded', function () {
    const chatBox = document.getElementById('chat-box');
    const loading = document.getElementById('loading');
    const input = document.getElementById('user-input');
    
    // --- PHẦN MỚI: XỬ LÝ UPLOAD FILE ---
    const fileInput = document.getElementById('file-upload');

    fileInput.addEventListener('change', async function() {
        const file = fileInput.files[0];
        if (!file) return;

        // 1. Hiện thông báo đang xử lý
        const str_time = formatTime(new Date());
        const loadingHtml = document.createElement('div');
        loadingHtml.className = 'd-flex justify-content-start mb-4';
        loadingHtml.innerHTML = `
            <div class="img_cont_msg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Logo_Bach_Mai_Hospital.png/600px-Logo_Bach_Mai_Hospital.png" class="rounded-circle user_img_msg"></div>
            <div class="msg_cotainer" style="background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba;">
                ⏳ Đang đọc tài liệu "<b>${file.name}</b>".<br>Vui lòng chờ khoảng 1-2 phút...
                <span class="msg_time">${str_time}</span>
            </div>`;
        chatBox.appendChild(loadingHtml);
        scrollToBottom();
        loading.style.display = 'block';

        // 2. Gửi file lên server
        const formData = new FormData();
        formData.append('file', file);

        try {
            const resp = await fetch('/upload_doc', {
                method: 'POST',
                body: formData
            });
            const data = await resp.json();
            
            loading.style.display = 'none';
            
            // 3. Hiện thông báo kết quả
            const resultHtml = document.createElement('div');
            resultHtml.className = 'd-flex justify-content-start mb-4';
            
            if (data.status === 'success') {
                resultHtml.innerHTML = `
                    <div class="img_cont_msg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Logo_Bach_Mai_Hospital.png/600px-Logo_Bach_Mai_Hospital.png" class="rounded-circle user_img_msg"></div>
                    <div class="msg_cotainer" style="background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb;">
                        ✅ ${data.message}
                        <span class="msg_time">${str_time}</span>
                    </div>`;
            } else {
                resultHtml.innerHTML = `
                    <div class="img_cont_msg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Logo_Bach_Mai_Hospital.png/600px-Logo_Bach_Mai_Hospital.png" class="rounded-circle user_img_msg"></div>
                    <div class="msg_cotainer" style="background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;">
                        ❌ Lỗi: ${data.message}
                        <span class="msg_time">${str_time}</span>
                    </div>`;
            }
            chatBox.appendChild(resultHtml);
            scrollToBottom();

        } catch (err) {
            loading.style.display = 'none';
            alert("Lỗi kết nối server khi upload!");
        }
        
        // Reset input để chọn lại file khác được
        fileInput.value = '';
    });
    // -----------------------------------

    function formatTime(d) {
        const hour = d.getHours();
        const minute = d.getMinutes();
        return hour + ':' + (minute < 10 ? '0' : '') + minute;
    }

    function scrollToBottom() {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function sendMessage() {
        const rawText = input.value && input.value.trim();
        if (!rawText) return;

        const str_time = formatTime(new Date());

        const userHtml = document.createElement('div');
        userHtml.className = 'd-flex justify-content-end mb-4';
        userHtml.innerHTML = `<div class="msg_cotainer_send">${escapeHtml(rawText)}<span class="msg_time_send">${str_time}</span></div><div class="img_cont_msg"><img src="https://cdn-icons-png.flaticon.com/512/1077/1077114.png" class="rounded-circle user_img_msg"></div>`;
        input.value = '';
        chatBox.appendChild(userHtml);
        scrollToBottom();

        loading.style.display = 'block';

        try {
            const resp = await fetch('/get_response', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ msg: rawText })
            });
            const data = await resp.json();
            loading.style.display = 'none';

            const botResponse = marked.parse(data.answer || '');
            const botHtml = document.createElement('div');
            botHtml.className = 'd-flex justify-content-start mb-4';
            botHtml.innerHTML = `<div class="img_cont_msg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Logo_Bach_Mai_Hospital.png/600px-Logo_Bach_Mai_Hospital.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer">${botResponse}<span class="msg_time">${str_time}</span></div>`;
            chatBox.appendChild(botHtml);
            scrollToBottom();
        } catch (err) {
            loading.style.display = 'none';
            const errHtml = document.createElement('div');
            errHtml.className = 'd-flex justify-content-start mb-4';
            errHtml.innerHTML = `<div class="img_cont_msg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Logo_Bach_Mai_Hospital.png/600px-Logo_Bach_Mai_Hospital.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer">Lỗi: ${escapeHtml(err.message)}<span class="msg_time">${str_time}</span></div>`;
            chatBox.appendChild(errHtml);
            scrollToBottom();
        }
    }

    window.sendMessage = sendMessage;

    input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });

    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/\"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
});