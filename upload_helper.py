"""
SoNoBot Hugging Face Upload Helper
Giúp upload code lên Hugging Face Spaces dễ dàng
"""

import os
import subprocess
import json
from datetime import datetime

def create_upload_script():
    """Tạo script upload tự động"""
    script_content = '''#!/bin/bash
# SoNoBot Hugging Face Upload Script
# Chạy script này để upload code lên Hugging Face

echo "🚀 Bắt đầu upload SoNoBot lên Hugging Face..."

# Kiểm tra git
if ! command -v git &> /dev/null; then
    echo "❌ Git chưa được cài đặt. Vui lòng cài đặt git trước."
    exit 1
fi

# Clone repository (nếu chưa có)
if [ ! -d "TT-hf" ]; then
    echo "📥 Clone repository..."
    git clone https://huggingface.co/spaces/kk1718/TT TT-hf
    cd TT-hf
else
    echo "📂 Repository đã tồn tại, pull latest..."
    cd TT-hf
    git pull origin main
fi

# Copy files
echo "📋 Copy files..."
cp ../app.py .
cp ../requirements.txt .
cp ../Dockerfile .
cp ../README.md .
cp ../.gitignore .

# Copy src directory
echo "📁 Copy src directory..."
rm -rf src/
cp -r ../src/ .

# Kiểm tra file
echo "🔍 Kiểm tra files..."
ls -la

# Git add
echo "➕ Git add files..."
git add .
git status

# Git commit
echo "💾 Git commit..."
COMMIT_MSG="Update SoNoBot with Gradio interface - Removed Reply Keyboard - $(date +'%Y-%m-%d %H:%M:%S')"
git commit -m "$COMMIT_MSG"

# Git push
echo "🚀 Git push..."
git push origin main

echo "✅ Upload hoàn tất!"
echo "🌐 Xem kết quả tại: https://huggingface.co/spaces/kk1718/TT"
'''
    
    with open('upload_to_hf.sh', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # Make executable on Unix systems
    try:
        os.chmod('upload_to_hf.sh', 0o755)
    except:
        pass
    
    return 'upload_to_hf.sh'

def create_windows_script():
    """Tạo script cho Windows"""
    script_content = '''@echo off
REM SoNoBot Hugging Face Upload Script for Windows
REM Chạy script này để upload code lên Hugging Face

echo 🚀 Bắt đầu upload SoNoBot lên Hugging Face...

REM Kiểm tra git
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Git chưa được cài đặt. Vui lòng cài đặt git trước.
    pause
    exit /b 1
)

REM Clone repository (nếu chưa có)
if not exist "TT-hf" (
    echo 📥 Clone repository...
    git clone https://huggingface.co/spaces/kk1718/TT TT-hf
    cd TT-hf
) else (
    echo 📂 Repository đã tồn tại, pull latest...
    cd TT-hf
    git pull origin main
)

REM Copy files
echo 📋 Copy files...
copy ..\\app.py .
copy ..\\requirements.txt .
copy ..\\Dockerfile .
copy ..\\README.md .
copy ..\\.gitignore .

REM Copy src directory
echo 📁 Copy src directory...
if exist src rmdir /s /q src
xcopy ..\\src src\\ /E /I /Y

REM Kiểm tra file
echo 🔍 Kiểm tra files...
dir

REM Git add
echo ➕ Git add files...
git add .
git status

REM Git commit
echo 💾 Git commit...
set COMMIT_MSG=Update SoNoBot with Gradio interface - Removed Reply Keyboard - %date% %time%
git commit -m "%COMMIT_MSG%"

REM Git push
echo 🚀 Git push...
git push origin main

echo ✅ Upload hoàn tất!
echo 🌐 Xem kết quả tại: https://huggingface.co/spaces/kk1718/TT
pause
'''
    
    with open('upload_to_hf.bat', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    return 'upload_to_hf.bat'

def create_manual_guide():
    """Tạo hướng dẫn thủ công chi tiết"""
    guide_content = '''
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
'''
    
    with open('UPLOAD_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    return 'UPLOAD_GUIDE.md'

def main():
    """Main function"""
    print("🛠️ Tạo các công cụ upload cho SoNoBot...")
    
    # Create upload scripts
    unix_script = create_upload_script()
    windows_script = create_windows_script()
    guide = create_manual_guide()
    
    print(f"✅ Đã tạo các file:")
    print(f"📜 {unix_script} - Script cho Linux/Mac")
    print(f"📜 {windows_script} - Script cho Windows")
    print(f"📖 {guide} - Hướng dẫn thủ công chi tiết")
    
    print("\n🎯 Hãy chọn 1 trong 3 cách:")
    print("1. Chạy upload_to_hf.sh (Linux/Mac)")
    print("2. Chạy upload_to_hf.bat (Windows)")
    print("3. Đọc UPLOAD_GUIDE.md và làm thủ công")
    
    print("\n⚠️ Lưu ý: Cần có Git được cài đặt và đăng nhập Hugging Face")

if __name__ == "__main__":
    main()
