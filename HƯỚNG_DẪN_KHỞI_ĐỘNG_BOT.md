# HƯỚNG DẪN CẤU TRÚC DỰ ÁN VÀ KHỞI ĐỘNG BOT

## 1. CẤU TRÚC DỰ ÁN

```
TT/
├── main.py                    # Điểm vào chính của bot
├── app.py                     # Giao diện Gradio (không bắt buộc)
├── start.bat                  # Script khởi động cho Windows CMD
├── start.ps1                  # Script khởi động cho Windows PowerShell
├── requirements.txt           # Danh sách các dependencies cần cài đặt
├── Dockerfile                 # Cấu hình Docker (không bắt buộc)
├── README.md                  # Tài liệu dự án chi tiết
├── .env.example               # Mẫu tệp cấu hình
└── src/
    ├── bot.py                 # Giao tiếp với SafeW API
    ├── config.py              # Quản lý cấu hình
    ├── database.py            # Quản lý database
    ├── handlers/
    │   └── commands.py        # Xử lý các lệnh bot
    ├── utils/
    │   ├── calculator.py      # Công cụ tính toán tài chính
    │   └── parser.py          # Công cụ phân tích tin nhắn
    └── ai/
        └── bigmodel.py        # Tích hợp AI Assistant
```

## 2. CÁC TỆP CHÍNH VÀ CHỨC NĂNG

### 2.1 main.py
- **Chức năng**: Đây là điểm vào chính của bot, tất cả quy trình khởi động bắt đầu từ đây.
- **Cấu trúc**: 
  - Khởi tạo logging
  - Class `SoNoBot`: Quản lý toàn bộ vòng đời của bot
  - Phương thức `initialize()`: Khởi tạo database, kết nối API, khởi động AI
  - Phương thức `handle_message()`: Xử lý từng tin nhắn
  - Phương thức `start_polling()`: Lắng nghe tin nhắn mới
  - Phương thức `start()`: Bắt đầu bot
  - Phương thức `stop()`: Dừng bot gracefully

### 2.2 src/config.py
- **Chức năng**: Quản lý cấu hình bot từ biến môi trường.
- **Biến môi trường cần thiết**:
  - `BOT_TOKEN`: Token bot SafeW (bắt buộc)
  - `DB_PATH`: Đường dẫn đến database (mặc định: sonobot.db)
  - `ADMIN_ID`: ID Telegram của admin (cách nhau bằng dấu phẩy)
  - `LOG_LEVEL`: Mức độ logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - `BIGMODEL_API_KEY`: API key của BigModel AI (tùy chọn)

### 2.3 src/bot.py
- **Chức năng**: Giao tiếp với SafeW API.
- **Tính năng**: Kết nối API, lấy tin nhắn, gửi tin nhắn, xử lý lệnh bot.

### 2.4 src/database.py
- **Chức năng**: Quản lý database SQLite.
- **Bảng dữ liệu**:
  - `users`: Lưu thông tin người dùng
  - `transactions`: Lưu thông tin giao dịch
- **Phương thức chính**: Thêm/xóa/gọi thông tin người dùng và giao dịch.

### 2.5 src/handlers/commands.py
- **Chức năng**: Xử lý các lệnh bot.
- **Lệnh chính**:
  - `/start`: Đăng ký và bắt đầu
  - `/help`: Xem hướng dẫn
  - `/about`: Thông tin về bot
  - `/status`: Thống kê (chỉ admin)
  - `/reset`: Reset giao dịch (chỉ admin)

### 2.6 src/utils/calculator.py
- **Chức năng**: Xử lý các biểu thức tính toán.
- **Định dạng hỗ trợ**:
  - `+50k`: Nạp 50.000
  - `-30+20`: Rút 50
  - `+30+20`: Nạp 50

## 3. BƯỚC KHỞI ĐỘNG BOT

### 3.1 Chuẩn bị môi trường

1. **Cài đặt Python 3.12+**: Đảm bảo đã cài Python phiên bản 3.12 trở lên
2. **Cài đặt dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Tạo tệp cấu hình**:
   ```bash
   copy .env.example .env
   ```
   Sau đó chỉnh sửa tệp `.env` với thông tin của bạn.

### 3.2 Khởi động bot

#### Cách 1: Sử dụng script khởi động (Windows)

- **Windows CMD**:
  ```cmd
  start.bat
  ```

- **Windows PowerShell**:
  ```powershell
  .\start.ps1
  ```

#### Cách 2: Chạy trực tiếp bằng Python

```bash
python main.py
```

#### Cách 3: Sử dụng Docker (không bắt buộc)

```bash
docker build -t sonobot .
docker run -d --name sonobot \
  -e BOT_TOKEN=your_token \
  -e ADMIN_ID=your_id \
  -e BIGMODEL_API_KEY=your_key \
  sonobot
```

## 4. QUY TRÌNH KHỞI ĐỘNG CHI TIẾT

Khi bạn chạy `python main.py`, quy trình khởi động diễn ra như sau:

1. **Khởi tạo logging**: Đặt up hệ thống logging
2. **Nạp cấu hình**: Đọc các biến môi trường từ tệp `.env`
3. **Khởi tạo database**: Tạo bảng users và transactions nếu chưa tồn tại
4. **Kết nối SafeW API**: Sử dụng BOT_TOKEN để kết nối
5. **Đặt các lệnh bot**: `/start` và `/help`
6. **Khởi động AI Assistant**: Nếu BIGMODEL_API_KEY được cung cấp
7. **Bắt đầu lắng nghe tin nhắn**: Bắt đầu polling để lấy các tin nhắn mới
8. **Xử lý tin nhắn**: Mỗi tin nhắn được xử lý theo luồng:
   - Đăng ký người dùng (nếu chưa có)
   - Kiểm tra nếu là biểu thức tính toán
   - Kiểm tra nếu là lệnh bot
   - Kiểm tra nếu là câu hỏi AI

## 5. KIỂM TRA TRẠNG THÁI BOT

Khi bot khởi động thành công, bạn sẽ thấy các thông báo:

```
🚀 Khởi tạo SoNoBot...
📊 Khởi tạo database...
🔗 Kết nối đến SafeW API...
✅ Bot đã khởi tạo thành công!
🔄 Bắt đầu lắng nghe tin nhắn...
🎉 SoNoBot đã khởi động thành công!
🤖 Bot name: SoNoBot
📊 Database: sonobot.db
👤 Admin IDs: [123456789]
```

## 6. CÁC LỖI THƯỜNG GẶP VÀ CÁCH KHẮC PHỤC

### 6.1 Lỗi "BOT_TOKEN is required!"
- **Nguyên nhân**: Chưa nhập BOT_TOKEN vào tệp `.env`
- **Giải pháp**: Mở tệp `.env` và thêm `BOT_TOKEN=your_bot_token_here`

### 6.2 Lỗi "Invalid BOT_TOKEN format!"
- **Nguyên nhân**: BOT_TOKEN không đúng định dạng
- **Giải pháp**: Đảm bảo token có dạng `123456789:abcdef...` (có chứa dấu colon)

### 6.3 Lỗi "ModuleNotFoundError"
- **Nguyên nhân**: Chưa cài đặt dependencies
- **Giải pháp**: Chạy `pip install -r requirements.txt`

### 6.4 Bot không phản hồi
- **Nguyên nhân**: Có thể là lỗi kết nối mạng hoặc token sai
- **Giải pháp**: Kiểm tra kết nối mạng và token trong tệp `.env`

## 7. TẠI LIỆU BỔ SUNG

- **Tài liệu chi tiết**: `README.md`
- **Giao diện Gradio**: Chạy `python app.py` để xem
- **Log bot**: Xem file `sonobot.log` để theo dõi hoạt động

---

**SoNoBot - Bot quản lý nợ cá nhân và nhóm**
