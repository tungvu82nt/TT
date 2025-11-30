# 🚀 UPLOAD SONOBOT LÊN HUGGING FACE - CỰC KỲ ĐƠN GIẢN

## 📋 CÁCH UPLOAD TRỰC TIẾP QUA WEB (KHÔNG CẦN GIT)

### Bước 1: Truy cập trang
- Mở trình duyệt: https://huggingface.co/spaces/kk1718/TT
- Đăng nhập bằng tài khoản kk1718

### Bước 2: Upload files (theo đúng thứ tự này)

**1. Upload file đơn lẻ - LÀM TỪNG FILE:**

1. Click **"Add file"** → **"Upload files"**
2. Chọn file: `app.py` → Upload
3. Điền commit: `"Add app.py"` → Commit
4. Lặp lại cho từng file:

```
📤 app.py → Commit: "Add app.py"
📤 requirements.txt → Commit: "Add requirements.txt"  
📤 Dockerfile → Commit: "Add Dockerfile"
📤 README.md → Commit: "Add README.md"
📤 .gitignore → Commit: "Add .gitignore"
```

**2. Upload thư mục src:**

1. Click **"Add file"** → **"Upload files"**
2. Chọn TOÀN BỘ file trong thư mục `src/`:
   - Giữ Ctrl và chọn tất cả file .py trong src
   - HOẶC kéo thả cả thư mục src vào
3. Đảm bảo giữ cấu trúc: `src/handlers/`, `src/utils/`, v.v.
4. Commit: `"Add src directory"`
5. Upload

### Bước 3: Kiểm tra kết quả
- Click tab **"App"** để xem giao diện Gradio
- Click **"Logs"** nếu có lỗi build
- Chờ 2-3 phút để build hoàn tất

### Bước 4: Test thử
- Giao diện web sẽ hiển thị ở: https://huggingface.co/spaces/kk1718/TT
- Nếu thấy giao diện Gradio → ✅ THÀNH CÔNG!

## 🔧 CÁCH SỬA SAU UPLOAD

### Sửa file nhanh:
1. Vào **"Files"**
2. Click file cần sửa 
3. Click **"Edit"** (biểu tượng bút chì)
4. Sửa code
5. **"Commit changes"**

### Upload lại file:
1. Xóa file cũ: Click file → **"Delete"**
2. Upload file mới: **"Add file"** → Upload

## ⚠️ LƯU Ý QUAN TRỌNG

### Trước khi upload:
- ✅ Đã xóa Reply Keyboard (theo yêu cầu)
- ✅ Code đang chạy tốt ở local
- ✅ Có đủ 6 thành phần: app.py, requirements.txt, Dockerfile, README.md, .gitignore, src/

### Khi upload:
- ✅ Upload từng file một (đỡ bị lỗi)
- ✅ Commit message rõ ràng
- ✅ Chờ build hoàn tất

### Nếu bị lỗi:
- ❌ **Build failed**: Xem tab **"Logs"** để biết lỗi
- ❌ **File missing**: Upload lại file đó
- ❌ **Structure wrong**: Xóa và upload lại đúng cấu trúc

## 🎯 SAU UPLOAD THÀNH CÔNG

Bạn sẽ có:
- 🌐 Giao diện web demo: https://huggingface.co/spaces/kk1718/TT
- 🤖 Bot Telegram vẫn chạy riêng: python main.py
- 📊 Cả 2 hoạt động độc lập

## 📞 HỖ TRỢ

Nếu gặp lỗi:
1. Kiểm tra tab **"Logs"** đầu tiên
2. Copy lỗi và hỏi tôi
3. Hoặc upload lại từ đầu

**Chúc upload thành công!** 🎉
