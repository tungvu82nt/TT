
# 📋 HƯỚNG DẪN UPLOAD SONOBOT LÊN HUGGING FACE (THỦ CÔNG)

## 🎯 Mục tiêu: Upload SoNoBot với Gradio interface

## 📁 Files cần upload:
1. app.py (Gradio interface)
2. requirements.txt (dependencies)
3. Dockerfile (container config)
4. README.md (documentation)
5. .gitignore (security)
6. src/ (source code directory)

## 🚀 Cách upload qua web interface:

### Bước 1: Truy cập
- Mở trình duyệt: https://huggingface.co/spaces/kk1718/TT
- Đăng nhập nếu cần

### Bước 2: Upload từng file
1. Click tab "Files" (trên cùng)
2. Click "Add file" → "Upload files"
3. Chọn file theo thứ tự:

**Upload file đơn lẻ:**
```
📤 upload app.py
📤 upload requirements.txt  
📤 upload Dockerfile
📤 upload README.md
📤 upload .gitignore
```

**Upload thư mục src:**
1. Click "Add file" → "Upload files"
2. Chọn TOÀN BỘ file trong thư mục src/
3. Đảm bảo giữ cấu trúc thư mục

### Bước 3: Commit
- Điền commit message: 
  `"Update SoNoBot with Gradio interface - Removed Reply Keyboard"`
- Click "Commit changes"

### Bước 4: Kiểm tra
- Click tab "App" để xem giao diện
- Click tab "Logs" nếu có lỗi
- Chờ 1-2 phút để build hoàn tất

## 🔧 Cách sửa sau upload:

### Sửa file:
1. Vào "Files" → Click file cần sửa
2. Click nút "Edit" (biểu tượng bút chì)
3. Sửa code trực tiếp
4. Commit changes

### Upload lại:
1. Xóa file cũ: Click file → "Delete"
2. Upload file mới: "Add file" → Upload

### Rollback:
1. Click tab "History"
2. Chọn version cũ
3. Click "Revert"

## ⚠️ Lưu ý:
- ✅ Đảm bảo upload đủ 6 thành phần chính
- ✅ Kiểm tra lại cấu trúc thư mục sau upload
- ✅ Commit message nên rõ ràng
- ✅ Chờ build hoàn tất trước khi test

## 🎉 Sau upload thành công:
- Space sẽ hiển thị giao diện Gradio
- Bot Telegram vẫn hoạt động riêng
- Có thể sửa trực tiếp trên web

Chúc bạn upload thành công! 🚀
