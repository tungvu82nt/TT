"""
SoNoBot Hugging Face Space Interface
Web interface for SoNoBot Telegram Debt Management Bot
"""

import gradio as gr
import os
import subprocess
import sys
from datetime import datetime

# Bot information
BOT_INFO = {
    "name": "SoNoBot",
    "version": "1.0.0",
    "description": "Bot quản lý nợ cá nhân và nhóm trên Telegram",
    "features": [
        "💰 Quản lý nợ - Ghi nhận ai nợ bạn bao nhiêu",
        "💸 Theo dõi trả nợ - Ghi lại khi bạn trả nợ", 
        "📊 Báo cáo tự động - Tổng hợp công nợ chi tiết",
        "🤖 AI Assistant - Hỗ trợ trả lời câu hỏi 24/7",
        "🧮 Tính toán thông minh - Hỗ trợ nhiều định dạng tiền tệ"
    ]
}

def get_bot_status():
    """Get current bot status"""
    return f"""
🤖 **SoNoBot Status**
⏰ **Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📊 **Database**: SQLite
🎯 **Features**: Debt Management, AI Assistant
🚀 **Status**: Ready to deploy on Telegram
    """

def get_commands_help():
    """Get commands help text"""
    return """
📝 **Danh sách lệnh SoNoBot:**

🔹 **Lệnh cơ bản:**
• `/start` - Đăng ký và bắt đầu
• `/help` - Xem hướng dẫn chi tiết
• `/about` - Thông tin về bot

🔹 **Quản lý nợ:**
• `/no @user [số tiền] [lý do]` - Ghi nhận nợ
• `/tra @user [số tiền]` - Ghi nhận trả nợ  
• `/check` - Xem báo cáo công nợ
• `/xoa [ID]` - Xóa giao dịch

💡 **Tính toán nhanh:**
• `+50k` - Nạp tiền 50,000đ
• `-100k` - Rút tiền 100,000đ
• `+1.5tr cafe` - Nạp tiền 1,5 triệu với ghi chú
    """

def create_interface():
    """Create Gradio interface"""
    
    with gr.Blocks(title="SoNoBot - Telegram Debt Management", theme=gr.themes.Soft()) as demo:
        
        gr.Markdown("# 🤖 SoNoBot - Bot Quản Lý Nợ Telegram")
        gr.Markdown("### 💰 Bot thông minh giúp quản lý nợ cá nhân và nhóm")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Image(
                    value=None,
                    label="SoNoBot Logo",
                    height=200
                )
                
                status_text = get_bot_status()
                status_output = gr.Textbox(
                    value=status_text,
                    label="📊 Trạng thái bot",
                    lines=8,
                    interactive=False
                )
                
                gr.Markdown("### 🔗 Thông tin kết nối")
                gr.Textbox(
                    value="https://t.me/SoNoBot",
                    label="Telegram Bot Link",
                    interactive=False
                )
                
            with gr.Column(scale=2):
                gr.Markdown("### 🎯 Tính năng chính")
                
                features_text = "\n".join([f"• {feature}" for feature in BOT_INFO["features"]])
                gr.Textbox(
                    value=features_text,
                    label="✨ Tính năng",
                    lines=6,
                    interactive=False
                )
                
                gr.Markdown("### 📝 Hướng dẫn sử dụng")
                
                help_text = get_commands_help()
                help_output = gr.Textbox(
                    value=help_text,
                    label="📋 Danh sách lệnh",
                    lines=15,
                    interactive=False
                )
                
                gr.Markdown("### 🛠️ Công nghệ")
                gr.Textbox(
                    value="Python 3.12+ • SafeW API • SQLite • BigModel AI • Async/Await",
                    label="⚙️ Stack công nghệ",
                    interactive=False
                )
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 📞 Liên hệ & Hỗ trợ")
                gr.Textbox(
                    value="📧 Email: kk1718@huggingface.co\n🌐 Space: https://huggingface.co/spaces/kk1718/TT",
                    label="📬 Thông tin liên hệ",
                    lines=3,
                    interactive=False
                )
                
            with gr.Column():
                gr.Markdown("### 🚀 Triển khai")
                gr.Textbox(
                    value="Bot đã sẵn sàng để triển khai trên Telegram!\nSử dụng BOT_TOKEN trong file .env để kích hoạt.",
                    label="🔧 Triển khai",
                    lines=3,
                    interactive=False
                )
        
        gr.Markdown("---")
        gr.Markdown("### 💡 Lưu ý")
        gr.Markdown("""
        - Đảm bảo cung cấp BOT_TOKEN trong file .env để bot hoạt động
        - Có thể tùy chỉnh ADMIN_ID để quản lý bot
        - BigModel API key là tùy chọn cho AI Assistant
        """)
        
        gr.Markdown("---")
        gr.Markdown("⭐ **Nếu thấy hữu ích, hãy cho ⭐ star để ủng hộ!**")
    
    return demo

if __name__ == "__main__":
    # Create and launch the interface
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_api=False
    )
