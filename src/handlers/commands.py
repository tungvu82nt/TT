"""
Command handlers for SoNoBot
Handles basic commands like /start, /help
"""

import logging
from typing import Dict, Optional
from ..bot import bot
from ..database import database
from ..config import config
from ..utils.parser import format_money

logger = logging.getLogger(__name__)

class CommandHandler:
    """Handler for basic bot commands"""
    
    @staticmethod
    async def handle_start(message: Dict) -> bool:
        """
        Handle /start command - Register user and show welcome message
        
        Args:
            message: Telegram message object
            
        Returns:
            bool: True if handled successfully
        """
        try:
            user_info = bot.extract_user_info(message)
            chat_info = bot.extract_chat_info(message)
            
            if not user_info:
                await bot.send_message(
                    chat_info['chat_id'],
                    "❌ Không thể lấy thông tin người dùng!"
                )
                return False
            
            # Register user in database
            success = await database.add_user(
                user_info['user_id'],
                user_info['username'],
                user_info['full_name']
            )
            
            if success:
                welcome_text = f"""
🎉 Chào mừng đến với SoNoBot!

📝 **SoNoBot** là bot quản lý nợ cá nhân và nhóm đơn giản.

🔹 **Các lệnh chính:**
• NẠP tiền (người khác nợ bạn)
• RÚT tiền (bạn trả nợ)
• Xem báo cáo nợ
• Xóa giao dịch
• Xem hướng dẫn

💡 **Mẹo:** Có thể viết tiền tệ ngắn gọn: `50k`, `1.5tr`, `200`

🚀 Bắt đầu quản lý nợ ngay!
                """.strip()
                
                await bot.send_message(
                    chat_info['chat_id'],
                    welcome_text
                )
                
                logger.info(f"User {user_info['username']} ({user_info['user_id']}) started bot")
                return True
            else:
                await bot.send_message(
                    chat_info['chat_id'],
                    "❌ Đã có lỗi xảy ra khi đăng ký. Vui lòng thử lại!"
                )
                return False
                
        except Exception as e:
            logger.error(f"Error handling /start: {e}")
            return False
    
    @staticmethod
    async def handle_help(message: Dict) -> bool:
        """
        Handle /help command - Show detailed help information
        
        Args:
            message: Telegram message object
            
        Returns:
            bool: True if handled successfully
        """
        try:
            chat_info = bot.extract_chat_info(message)
            
            if not chat_info:
                return False
            
            help_text = """
🤖 **SoNoBot - Hướng dẫn sử dụng**

📋 **DANH SÁCH LỆNH:**

🔹 **Bắt đầu**
• `/start` - Đăng ký tài khoản
• `/help` - Xem hướng dẫn này

🔹 **Quản lý nợ**
• `/no @user [số tiền] [lý do]` - NẠP tiền (người khác nợ bạn)
  Ví dụ: `/no @nam 50k cafe`
  
• `/tra @user [số tiền]` - RÚT tiền (bạn trả nợ)
  Ví dụ: `/tra @nam 50k`

• `/check` - Xem báo cáo công nợ chi tiết

🔹 **Quản lý giao dịch**
• `/xoa [ID_giao_dịch]` - Xóa giao dịch (chỉ chủ nợ mới xóa được)
  Ví dụ: `/xoa 12`

💡 **Định dạng tiền tệ:**
• `50k` → 50,000đ
• `1.5tr` → 1,500,000đ
• `200` → 200đ
• `100k`, `50k` (nhiều số)

📝 **Ví dụ thực tế:**
1. NẠP tiền (bạn cafe):
   `/no @anh 35k cafe sáng`

2. RÚT tiền (trả cà phê):
   `/tra @anh 35k`

3. Kiểm tra công nợ:
   `/check`

⚠️ **Lưu ý:**
• Bot chỉ hoạt động trong group/chat có @menntioned
• Cần đăng ký bằng `/start` trước khi sử dụng
• Chỉ chủ nợ mới được xóa giao dịch

❓ **Cần hỗ trợ?**
Vui lòng liên hệ admin của bot.
            """.strip()
            
            await bot.send_message(
                chat_info['chat_id'],
                help_text
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error handling /help: {e}")
            return False
    
    @staticmethod
    async def handle_about(message: Dict) -> bool:
        """
        Handle /about command - Show bot information
        
        Args:
            message: Telegram message object
            
        Returns:
            bool: True if handled successfully
        """
        try:
            chat_info = bot.extract_chat_info(message)
            
            if not chat_info:
                return False
            
            about_text = """
🤖 **SoNoBot - Bot Quản Lý Nợ**

📝 **Phiên bản:** 1.0.0
🛠️ **Công nghệ:** SafeW API + Python
💾 **Database:** SQLite

🎯 **Tính năng:**
• Ghi nhận nợ/trả nợ
• Báo cáo công nợ tự động
• Quản lý giao dịch
• Hỗ trợ format tiền Việt

🚀 **Được phát triển bởi:** SoNoBot Team
📖 **Nguồn mở:** GitHub Repository
            """.strip()
            
            await bot.send_message(
                chat_info['chat_id'],
                about_text
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error handling /about: {e}")
            return False
    
    @staticmethod
    async def handle_status(message: Dict) -> bool:
        """
        Handle /status command - Show bot status (admin only)
        
        Args:
            message: Telegram message object
            
        Returns:
            bool: True if handled successfully
        """
        try:
            user_info = bot.extract_user_info(message)
            chat_info = bot.extract_chat_info(message)
            
            if not user_info or not chat_info:
                return False
            
            # Check if user is admin
            if not config.is_admin(user_info['user_id']):
                await bot.send_message(
                    chat_info['chat_id'],
                    "❌ Lệnh này chỉ dành cho admin!"
                )
                return False
            
            # Get database statistics
            try:
                # Count users (simplified - would need async context)
                user_count = 0  # Would need to implement count_users method
                
                status_text = f"""
📊 **Bot Status Report**

🤖 **Bot Information:**
• Name: {config.BOT_NAME}
• API: SafeW
• Status: 🟢 Online

👥 **Statistics:**
• Total Users: {user_count}
• Database: {config.DB_PATH}
• Log Level: {config.LOG_LEVEL}

⚙️ **Configuration:**
• Admin IDs: {', '.join(map(str, config.ADMIN_IDS)) if config.ADMIN_IDS else 'None'}
• Token: {'✅ Valid' if config.BOT_TOKEN else '❌ Missing'}
                """.strip()
                
                await bot.send_message(
                    chat_info['chat_id'],
                    status_text
                )
                
                return True
                
            except Exception as e:
                await bot.send_message(
                    chat_info['chat_id'],
                    f"❌ Lỗi khi lấy thống kê: {str(e)}"
                )
                return False
                
        except Exception as e:
            logger.error(f"Error handling /status: {e}")
            return False
    
    @staticmethod
    async def handle_reset(message: Dict) -> bool:
        """
        Handle /reset command - Reset all transaction data (admin only)
        
        Args:
            message: Telegram message object
            
        Returns:
            bool: True if handled successfully
        """
        try:
            user_info = bot.extract_user_info(message)
            chat_info = bot.extract_chat_info(message)
            
            if not user_info or not chat_info:
                return False
            
            # Check if user is admin
            if not config.is_admin(user_info['user_id']):
                await bot.send_message(
                    chat_info['chat_id'],
                    "❌ **Lệnh này chỉ dành cho admin!**\n\n"
                    "⚠️ Chỉ quản trị viên mới có quyền reset dữ liệu."
                )
                return False
            
            # Get transaction count before reset
            transaction_count = await database.get_transaction_count()
            
            # Confirm reset
            if transaction_count == 0:
                await bot.send_message(
                    chat_info['chat_id'],
                    "ℹ️ **Không có dữ liệu để reset!**\n\n"
                    "📊 Hiện tại không có giao dịch nào trong hệ thống."
                )
                return True
            
            # Perform reset
            success = await database.reset_all_transactions()
            
            if success:
                reset_text = (
                    f"╔═══════════════════════════════╗\n"
                    f"║  🔄 RESET DỮ LIỆU THÀNH CÔNG  ║\n"
                    f"╚═══════════════════════════════╝\n\n"
                    f"✅ **Đã xóa:** `{transaction_count}` giao dịch\n"
                    f"📊 **Trạng thái:** Tất cả dữ liệu đã được reset về 0\n\n"
                    f"⚠️ **Lưu ý:** Hành động này không thể hoàn tác!\n"
                    f"💾 Dữ liệu người dùng (users) vẫn được giữ nguyên."
                )
                
                await bot.send_message(
                    chat_info['chat_id'],
                    reset_text,
                    parse_mode="Markdown"
                )
                
                logger.warning(f"Admin {user_info['username']} (ID: {user_info['user_id']}) reset all transactions")
                return True
            else:
                await bot.send_message(
                    chat_info['chat_id'],
                    "❌ **Lỗi khi reset dữ liệu!**\n\n"
                    "Vui lòng thử lại hoặc liên hệ developer."
                )
                return False
                
        except Exception as e:
            logger.error(f"Error handling /reset: {e}")
            return False


# Dictionary mapping commands to handlers
COMMAND_HANDLERS = {
    '/start': CommandHandler.handle_start,
    '/help': CommandHandler.handle_help,
    '/about': CommandHandler.handle_about,
    '/status': CommandHandler.handle_status,
    '/reset': CommandHandler.handle_reset,
}

async def handle_command(message: Dict) -> bool:
    """
    Route command to appropriate handler
    
    Args:
        message: Telegram message object
        
    Returns:
        bool: True if command was handled
    """
    text_content = bot.extract_text_content(message)
    
    if not text_content or not text_content.startswith('/'):
        return False
    
    # Parse command
    command_info = bot.parse_command(text_content)
    if not command_info:
        return False
    
    command, args = command_info
    
    # Find handler for command
    handler = COMMAND_HANDLERS.get(command)
    if handler:
        return await handler(message)
    else:
        # Unknown command
        chat_info = bot.extract_chat_info(message)
        if chat_info:
            await bot.send_message(
                chat_info['chat_id'],
                f"❌ Lệnh không hợp lệ: `{command}`\n"
                "Gõ `/help` để xem danh sách lệnh hỗ trợ."
            )
        return False
