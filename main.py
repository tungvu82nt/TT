#!/usr/bin/env python3
"""
SoNoBot - SafeW Telegram Debt Management Bot
Main entry point for the bot
"""

import asyncio
import logging
import signal
import sys
from typing import Optional

# Import bot modules
from src.bot import bot
from src.database import database
from src.config import config
from src.utils.parser import format_money
from src.ai.bigmodel import BigModelAI

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('sonobot.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)

class SoNoBot:
    """Main bot application"""
    
    def __init__(self):
        self.running = False
        self.polling_task: Optional[asyncio.Task] = None
        self.ai: Optional[BigModelAI] = None
    
    async def initialize(self):
        """Initialize bot components"""
        try:
            logger.info("🚀 Khởi tạo SoNoBot...")
            
            # Initialize database
            logger.info("📊 Khởi tạo database...")
            await database.init_db()
            
            # Initialize bot connection
            logger.info("🔗 Kết nối đến SafeW API...")
            await bot.start()
            
            # Set simple bot commands
            commands = [
                {"command": "start", "description": "Bắt đầu"},
                {"command": "help", "description": "Hướng dẫn"},
            ]
            
            await bot.set_my_commands(commands)
            
            # Initialize AI if API key is available
            if config.BIGMODEL_API_KEY:
                logger.info("🧠 Khởi tạo AI Assistant...")
                self.ai = BigModelAI(
                    api_key=config.BIGMODEL_API_KEY,
                    api_url=config.BIGMODEL_API_URL
                )
                logger.info("✅ AI Assistant đã khởi tạo thành công!")
            else:
                logger.info("⚠️ AI API key not provided, AI features disabled")
            
            logger.info("✅ Bot đã khởi tạo thành công!")
            
        except Exception as e:
            logger.error(f"❌ Lỗi khởi tạo bot: {e}")
            raise
    
    async def handle_message(self, message: dict):
        """
        Handle incoming message
        
        Args:
            message: Telegram message object
        """
        try:
            # Skip if message is empty
            if not message:
                return
            
            text_content = bot.extract_text_content(message)
            chat_info = bot.extract_chat_info(message)
            
            # Auto-register user
            user_info = bot.extract_user_info(message)
            if user_info:
                await database.add_user(
                    user_info['user_id'],
                    user_info['username'],
                    user_info['full_name']
                )
                
            # Log incoming message
            if text_content and chat_info:
                username = f"@{user_info['username']}" if (user_info and user_info.get('username')) else f"{user_info.get('full_name', 'Anonymous')}" if user_info else "Anonymous"
                chat_type = chat_info.get('type', 'unknown')
                logger.info(f"📥 Tin nhắn từ {username} (ID: {user_info['user_id'] if user_info else 'unknown'}) trong {chat_type} chat ID {chat_info.get('chat_id', 'unknown')}: '{text_content}'")

            if not text_content:
                return

            # Handle calculation expressions
            try:
                from src.utils.calculator import parse_calculation, generate_calculation_help
                from datetime import datetime
            except ImportError:
                return
            
            calc_result = parse_calculation(text_content)
            
            if calc_result:
                # Ensure user_info exists
                if not user_info:
                    logger.warning("User info not available for calculation")
                    return
                
                amount, operation, note = calc_result
                
                # Check for ForceReply context
                reply_to = message.get('reply_to_message')
                if reply_to and 'text' in reply_to:
                    reply_text = reply_to['text']
                    if "💰 **NẠP TIỀN**" in reply_text:
                        operation = 'add'
                        # Treat amount as absolute value for deposit
                        amount = abs(amount)
                    elif "💸 **RÚT TIỀN**" in reply_text:
                        operation = 'subtract'
                        # Treat amount as absolute value for withdrawal
                        amount = abs(amount)
                
                user_id = user_info['user_id']
                
                # Save transaction and get total
                current_date = datetime.now().strftime("%d/%m/%Y")
                
                if operation in ['add', 'add_debt']:
                    # User NẠP (User -> System/Group)
                    await database.add_transaction(0, user_id, amount, note)
                    totals = await database.get_total_deposit_and_withdrawal(user_id)
                    # Format username display
                    username_display = f"@{user_info['username']}" if user_info.get('username') else user_info.get('full_name', 'User')
                    # Beautiful formatted response with emoji and markdown
                    response_text = (
                        f"╔═══════════════════════════════╗\n"
                        f"║  💰 GIAO DỊCH NẠP TIỀN        ║\n"
                        f"╚═══════════════════════════════╝\n\n"
                        f"👤 **USER:** `{username_display}`\n"
                        f"🆔 **ID:** `{user_id}`\n"
                        f"📅 **Ngày:** `{current_date}`\n\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"✅ **KẾT QUẢ:** `{format_money(amount)}`\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                        f"📊 **TỔNG KẾT:**\n"
                        f"💰 TỔNG NẠP: `{format_money(totals['total_nap'])}`\n"
                        f"💸 TỔNG RÚT: `{format_money(totals['total_rut'])}`\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"🎯 **TỔNG:** `{format_money(totals['total'])}`"
                    )
                    
                elif operation in ['subtract', 'payment']:
                    # User RÚT (System/Group -> User)
                    await database.add_transaction(user_id, 0, amount, note)
                    totals = await database.get_total_deposit_and_withdrawal(user_id)
                    # Format username display
                    username_display = f"@{user_info['username']}" if user_info.get('username') else user_info.get('full_name', 'User')
                    # Beautiful formatted response with emoji and markdown
                    response_text = (
                        f"╔═══════════════════════════════╗\n"
                        f"║  💸 GIAO DỊCH RÚT TIỀN        ║\n"
                        f"╚═══════════════════════════════╝\n\n"
                        f"👤 **USER:** `{username_display}`\n"
                        f"🆔 **ID:** `{user_id}`\n"
                        f"📅 **Ngày:** `{current_date}`\n\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"✅ **KẾT QUẢ:** `{format_money(amount)}`\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                        f"📊 **TỔNG KẾT:**\n"
                        f"💰 TỔNG NẠP: `{format_money(totals['total_nap'])}`\n"
                        f"💸 TỔNG RÚT: `{format_money(totals['total_rut'])}`\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"🎯 **TỔNG:** `{format_money(totals['total'])}`"
                    )
                
                logger.info(f"📤 Phản hồi giao dịch cho {user_id}: {operation} {amount}đ {f'- ghi chú: {note}' if note else ''}")
                
                # Inline Keyboard for quick actions
                inline_keyboard = {
                    "inline_keyboard": [
                        [
                            {"text": "NẠP 💰", "callback_data": "cmd_deposit"},
                            {"text": "RÚT 💸", "callback_data": "cmd_withdraw"}
                        ]
                    ]
                }
                
                await bot.send_message(chat_info['chat_id'], response_text, parse_mode="Markdown", reply_markup=inline_keyboard)
                return

            # Handle commands
            if text_content.startswith('/'):
                # Try to handle via command handlers
                from src.handlers.commands import handle_command
                handled = await handle_command(message)
                if handled:
                    return
                
                # Handle /start or /help (fallback)
                if text_content.strip().lower() in ['/start', '/help', 'help', 'hướng dẫn']:
                    if self.ai and (text_content.strip().lower() in ['help', 'hướng dẫn']):
                        # Use AI to generate contextual help
                        ai_help = await self.ai.get_help_response(text_content)
                        await bot.send_message(chat_info['chat_id'], ai_help)
                    else:
                        help_text = generate_calculation_help()
                        await bot.send_message(chat_info['chat_id'], help_text)
                    return

            # Handle AI questions (messages that start with ai:, bot:, or are questions)
            if self.ai and (
                text_content.lower().startswith(('ai:', 'bot:', 'hỏi:')) or 
                '?' in text_content or 
                text_content.lower().startswith('tại sao') or
                text_content.lower().startswith('làm sao')
            ):
                # Extract the actual question (remove prefix if present)
                question = text_content
                for prefix in ['ai:', 'bot:', 'hỏi:']:
                    if question.lower().startswith(prefix):
                        question = question[len(prefix):].strip()
                        break
                
                # Get AI response
                logger.info(f"🤖 Xử lý câu hỏi AI từ {user_info['user_id']}: '{question}'")
                ai_response = await self.ai.get_help_response(question)
                if ai_response:
                    logger.info(f"🤖 Phản hồi AI cho {user_info['user_id']} đã gửi")
                    await bot.send_message(chat_info['chat_id'], ai_response)
                    return
                    
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    async def start_polling(self):
        """Start polling for updates"""
        logger.info("🔄 Bắt đầu lắng nghe tin nhắn...")
        self.running = True
        
        while self.running:
            try:
                # Get updates from SafeW API
                updates_response = await bot.get_updates(timeout=10)
                
                if updates_response and updates_response.get('ok'):
                    updates = updates_response.get('result', [])
                    
                    for update in updates:
                        if self.running:
                            await self.handle_update(update)
                else:
                    # No updates, just continue
                    pass
                
            except asyncio.CancelledError:
                logger.info("Polling task cancelled")
                break
            except Exception as e:
                logger.error(f"Error in polling loop: {e}")
                # Wait a bit before retrying
                await asyncio.sleep(1)
    
    async def handle_update(self, update: dict):
        """Handle incoming update"""
        if 'message' in update:
            await self.handle_message(update['message'])
        elif 'callback_query' in update:
            await self.handle_callback_query(update['callback_query'])

    async def handle_callback_query(self, callback_query: dict):
        """Handle callback query"""
        try:
            query_id = callback_query['id']
            data = callback_query.get('data')
            message = callback_query.get('message')
            
            if not data or not message:
                return

            chat_id = message['chat']['id']
            
            # Answer callback to stop loading state
            await bot.answer_callback_query(query_id)

            if data == "cmd_deposit":
                await bot.send_message(
                    chat_id,
                    "💰 **NẠP TIỀN**\n"
                    "Nhập số tiền hoặc phép tính (ví dụ: `50k`, `10+20`):",
                    reply_markup={'force_reply': True, 'input_field_placeholder': 'Ví dụ: 50k hoặc 10+20'}
                )
            
            elif data == "cmd_withdraw":
                await bot.send_message(
                    chat_id,
                    "💸 **RÚT TIỀN**\n"
                    "Nhập số tiền hoặc phép tính (ví dụ: `50k`, `10+20`):",
                    reply_markup={'force_reply': True, 'input_field_placeholder': 'Ví dụ: 50k hoặc 10+20'}
                )
                
        except Exception as e:
            logger.error(f"Error handling callback query: {e}")

    async def start(self):
        """Start the bot"""
        try:
            # Initialize components
            await self.initialize()
            
            # Start polling in background task
            self.running = True
            self.polling_task = asyncio.create_task(self.start_polling())
            
            logger.info("🎉 SoNoBot đã khởi động thành công!")
            logger.info(f"🤖 Bot name: {config.BOT_NAME}")
            logger.info(f"📊 Database: {config.DB_PATH}")
            admin_ids_str = ', '.join(map(str, config.ADMIN_IDS)) if config.ADMIN_IDS else 'None'
            logger.info(f"👤 Admin IDs: {admin_ids_str}")
            
            # Keep the main coroutine running
            while self.running:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Fatal error in start(): {e}")
            raise

    async def stop(self):
        """Stop the bot gracefully"""
        logger.info("🛑 Đang dừng SoNoBot...")
        
        self.running = False
        
        # Cancel polling task
        if self.polling_task:
            self.polling_task.cancel()
            try:
                await self.polling_task
            except asyncio.CancelledError:
                pass
        
        # Close connections
        await bot.close()
        await database.close()
        
        logger.info("✅ SoNoBot đã dừng hoàn toàn.")

async def main():
    """Main entry point"""
    bot_app = SoNoBot()
    
    # Setup signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        bot_app.running = False
    
    try:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    except ValueError:
        logger.warning("Cannot set signal handlers (Windows limitation)")
    
    try:
        await bot_app.start()
    except KeyboardInterrupt:
        logger.info("Nhận tín hiệu Ctrl+C")
    except Exception as e:
        logger.error(f"Lỗi không xử lý được: {e}")
        sys.exit(1)
    finally:
        await bot_app.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 SoNoBot đã dừng!")
    except Exception as e:
        logger.error(f"❌ Lỗi khởi động bot: {e}")
        sys.exit(1)