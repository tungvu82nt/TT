@echo off
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
copy ..\app.py .
copy ..\requirements.txt .
copy ..\Dockerfile .
copy ..\README.md .
copy ..\.gitignore .

REM Copy src directory
echo 📁 Copy src directory...
if exist src rmdir /s /q src
xcopy ..\src src\ /E /I /Y

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
