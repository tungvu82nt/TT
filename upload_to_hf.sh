#!/bin/bash
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
