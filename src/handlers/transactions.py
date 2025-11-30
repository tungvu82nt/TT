"""
Transaction handlers for SoNoBot
Handles debt-related commands: /no, /tra, /check, /xoa
"""

import logging
from typing import Dict, Optional, List
from ..bot import bot
from ..database import database
from ..utils.parser import parse_money, extract_mentions, format_money, validate_username, sanitize_text

logger = logging.getLogger(__name__)

class TransactionHandler:
    """Handler for debt-related transactions"""
    
    @staticmethod
    async def handle_no(message: Dict) -> bool:
        """
        Handle /no command - Record debt (someone owes money to user)
        
        Args:
            message: Telegram message object
            
        Returns:
            bool: True if handled successfully
        """
        try:
            user_info = bot.extract_user_info(message)
            chat_info = bot.extract_chat_info(message)
            text_content = bot.extract_text_content(message)
            
            if not user_info or not chat_info or not text_content:
                return False
            
            # Parse command: /no @user [amount] [note]
            command_info = bot.parse_command(text_content)
            if not command_info:
                return False
            
            command, args = command_info
            args_parts = args.strip().split(maxsplit=2) if args else []
            
            if len(args_parts) < 2:
                await bot.send_message(
                    chat_info['chat_id'],
                    "❌ Sai cú pháp!\n"
                    "Đúng: `/no @user [số tiền] [lý do]`\n"
                    "Ví dụ: `/no @nam 50k cafe`"
                )
                return False
            
            # Extract debtor username
            debtor_mention = args_parts[0].strip()
            if not debtor_mention.startswith('@'):
                await bot.send_message(
                    chat_info['chat_id'],
                    "❌ Phải @mention người nợ!\n"
                    "Ví dụ: `/no @nam 50k`"
                )
                return False
            
            debtor_username = debtor_mention[1:].strip()  # Remove @
            
            # Validate username
            if not validate_username(debtor_username):
                await bot.send_message(
                    chat_info['chat_id'],
                    f"❌ Tên người dùng không hợp lệ: `@{debtor_username}`"
                )
                return False
            
            # Parse amount
            try:
                amount = parse_money(args_parts[1])
            except ValueError as e:
                await bot.send_message(
                    chat_info['chat_id'],
                    f"❌ Số tiền không hợp lệ: `{args_parts[1]}`\n"
                    f"Lỗi: {str(e)}\n"
                    "Ví dụ: `50k`, `1.5tr`, `200`"
                )
                return False
            
            # Extract note (optional)
            note = sanitize_text(args_parts[2]) if len(args_parts) > 2 else None
            
            # Get debtor user info from database
            debtor = await database.get_user_by_username(debtor_username)
            if not debtor:
                await bot.send_message(
                    chat_info['chat_id'],
                    f"❌ Không tìm thấy người dùng `@{debtor_username}`!\n"
                    "Người dùng này cần dùng `/start` với bot trước."
                )
                return False
            
            # Record the transaction
            creditor_id = user_info['user_id']  # Current user
            debtor_id = debtor['user_id']
            
            transaction_id = await database.add_transaction(
                debtor_id=debtor_id,
                creditor_id=creditor_id,
                amount=amount,
                note=note
            )
            
            if transaction_id:
                # Success message
                debtor_name = debtor['full_name'] or f"@{debtor_username}"
                creditor_name = user_info['full_name'] or "bạn"
                amount_formatted = format_money(amount)
                note_text = f" ({note})" if note else ""
                
                success_text = f"""
✅ **NẠP tiền thành công!**

📝 **Chi tiết giao dịch #{transaction_id}:**
• Người nợ: {debtor_name}
• Chủ nợ: {creditor_name}
• Số tiền: {amount_formatted}
• Lý do: {note or 'Không có'}

🔗 @{debtor_username} hiện nợ bạn thêm {amount_formatted}
                """.strip()
                
                await bot.send_message(
                    chat_info['chat_id'],
                    success_text
                )
                
                logger.info(f"Deposit recorded: @{debtor_username} owes @{user_info['username']} {amount_formatted} (ID: {transaction_id})")
                return True
            else:
                await bot.send_message(
                    chat_info['chat_id'],
                    "❌ Đã có lỗi xảy ra khi NẠP tiền. Vui lòng thử lại!"
                )
                return False
                
        except Exception as e:
            logger.error(f"Error handling /no: {e}")
            return False
    
    @staticmethod
    async def handle_tra(message: Dict) -> bool:
        """
        Handle /tra command - Record debt repayment
        
        Args:
            message: Telegram message object
            
        Returns:
            bool: True if handled successfully
        """
        try:
            user_info = bot.extract_user_info(message)
            chat_info = bot.extract_chat_info(message)
            text_content = bot.extract_text_content(message)
            
            if not user_info or not chat_info or not text_content:
                return False
            
            # Parse command: /tra @user [amount]
            command_info = bot.parse_command(text_content)
            if not command_info:
                return False
            
            command, args = command_info
            args_parts = args.strip().split(maxsplit=1) if args else []
            
            if len(args_parts) < 2:
                await bot.send_message(
                    chat_info['chat_id'],
                    "❌ Sai cú pháp!\n"
                    "Đúng: `/tra @user [số tiền]`\n"
                    "Ví dụ: `/tra @nam 50k`"
                )
                return False
            
            # Extract creditor username
            creditor_mention = args_parts[0].strip()
            if not creditor_mention.startswith('@'):
                await bot.send_message(
                    chat_info['chat_id'],
                    "❌ Phải @mention người nhận tiền!\n"
                    "Ví dụ: `/tra @nam 50k`"
                )
                return False
            
            creditor_username = creditor_mention[1:].strip()  # Remove @
            
            # Validate username
            if not validate_username(creditor_username):
                await bot.send_message(
                    chat_info['chat_id'],
                    f"❌ Tên người dùng không hợp lệ: `@{creditor_username}`"
                )
                return False
            
            # Parse amount
            try:
                amount = parse_money(args_parts[1])
            except ValueError as e:
                await bot.send_message(
                    chat_info['chat_id'],
                    f"❌ Số tiền không hợp lệ: `{args_parts[1]}`\n"
                    f"Lỗi: {str(e)}\n"
                    "Ví dụ: `50k`, `1.5tr`, `200`"
                )
                return False
            
            # Get creditor user info from database
            creditor = await database.get_user_by_username(creditor_username)
            if not creditor:
                await bot.send_message(
                    chat_info['chat_id'],
                    f"❌ Không tìm thấy người dùng `@{creditor_username}`!\n"
                    "Người dùng này cần dùng `/start` với bot trước."
                )
                return False
            
            # Record the repayment transaction (negative amount)
            creditor_id = creditor['user_id']
            debtor_id = user_info['user_id']  # Current user
            
            transaction_id = await database.add_transaction(
                debtor_id=debtor_id,
                creditor_id=creditor_id,
                amount=amount,
                note=f"RÚT tiền bởi @{user_info['username']}"
            )
            
            if transaction_id:
                # Success message
                creditor_name = creditor['full_name'] or f"@{creditor_username}"
                debtor_name = user_info['full_name'] or "bạn"
                amount_formatted = format_money(amount)
                
                success_text = f"""
✅ **RÚT tiền thành công!**

📝 **Chi tiết giao dịch #{transaction_id}:**
• Người rút: {debtor_name}
• Người nhận: {creditor_name}
• Số tiền: {amount_formatted}

🔗 Bạn đã rút cho @{creditor_username} số tiền {amount_formatted}
                """.strip()
                
                await bot.send_message(
                    chat_info['chat_id'],
                    success_text
                )
                
                logger.info(f"Withdrawal recorded: @{user_info['username']} withdrew to @{creditor_username} {amount_formatted} (ID: {transaction_id})")
                return True
            else:
                await bot.send_message(
                    chat_info['chat_id'],
                    "❌ Đã có lỗi xảy ra khi RÚT tiền. Vui lòng thử lại!"
                )
                return False
                
        except Exception as e:
            logger.error(f"Error handling /tra: {e}")
            return False
    
    @staticmethod
    async def handle_check(message: Dict) -> bool:
        """
        Handle /check command - Show debt summary
        
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
            
            # Get user's debt summary
            user_id = user_info['user_id']
            debt_summary = await database.get_user_debts(user_id)
            detailed_debts = await database.get_detailed_debts(user_id)
            
            # Format the report
            others_owe = debt_summary['others_owe_me']
            user_owes = debt_summary['i_owe_others']
            net_balance = debt_summary['net_balance']
            
            # Emoji indicators
            if net_balance > 0:
                balance_emoji = "📈"
                balance_text = f"Bạn thu về {format_money(net_balance)}"
            elif net_balance < 0:
                balance_emoji = "📉"
                balance_text = f"Bạn phải trả {format_money(abs(net_balance))}"
            else:
                balance_emoji = "⚖️"
                balance_text = "Đã cân bằng"
            
            report_text = f"""
📊 **Báo cáo công nợ của {user_info['full_name'] or 'bạn'}**

{balance_emoji} **Tổng quan:**
• Người khác nợ bạn: {format_money(others_owe)}
• Bạn nợ người khác: {format_money(user_owes)}
• **Thặng dư:** {balance_text}
            """.strip()
            
            # Add detailed debtors list
            if detailed_debts['debtors']:
                report_text += "\n\n💰 **Danh sách người nợ bạn:**"
                for debtor in detailed_debts['debtors']:
                    name = debtor['full_name'] or f"@{debtor['username']}"
                    report_text += f"\n• {name}: {format_money(debtor['amount'])}"
            
            # Add detailed creditors list
            if detailed_debts['creditors']:
                report_text += "\n\n💸 **Danh sách bạn nợ:**"
                for creditor in detailed_debts['creditors']:
                    name = creditor['full_name'] or f"@{creditor['username']}"
                    report_text += f"\n• {name}: {format_money(creditor['amount'])}"
            
            # Add tips
            if net_balance != 0:
                report_text += "\n\n💡 **Gợi ý:**"
                if net_balance > 0:
                    report_text += f"\n• Sử dụng `/tra @user [số tiền]` để ghi nhận RÚT tiền từ người khác"
                else:
                    report_text += f"\n• Sử dụng `/tra @user [số tiền]` để ghi nhận bạn RÚT tiền"
            
            await bot.send_message(
                chat_info['chat_id'],
                report_text
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error handling /check: {e}")
            return False
    
    @staticmethod
    async def handle_xoa(message: Dict) -> bool:
        """
        Handle /xoa command - Delete transaction (creditor only)
        
        Args:
            message: Telegram message object
            
        Returns:
            bool: True if handled successfully
        """
        try:
            user_info = bot.extract_user_info(message)
            chat_info = bot.extract_chat_info(message)
            text_content = bot.extract_text_content(message)
            
            if not user_info or not chat_info or not text_content:
                return False
            
            # Parse command: /xoa [transaction_id]
            command_info = bot.parse_command(text_content)
            if not command_info:
                return False
            
            command, args = command_info
            args = args.strip()
            
            if not args:
                await bot.send_message(
                    chat_info['chat_id'],
                    "❌ Sai cú pháp!\n"
                    "Đúng: `/xoa [ID_giao_dịch]`\n"
                    "Ví dụ: `/xoa 12`\n\n"
                    "💡 Dùng `/check` để xem ID các giao dịch gần nhất."
                )
                return False
            
            # Parse transaction ID
            try:
                transaction_id = int(args)
                if transaction_id <= 0:
                    raise ValueError("ID must be positive")
            except ValueError:
                await bot.send_message(
                    chat_info['chat_id'],
                    f"❌ ID giao dịch không hợp lệ: `{args}`\n"
                    "ID phải là số nguyên dương."
                )
                return False
            
            # Get transaction details first
            transaction = await database.get_transaction(transaction_id)
            if not transaction:
                await bot.send_message(
                    chat_info['chat_id'],
                    f"❌ Không tìm thấy giao dịch ID `{transaction_id}`"
                )
                return False
            
            # Check if user is creditor
            if transaction['creditor_id'] != user_info['user_id']:
                await bot.send_message(
                    chat_info['chat_id'],
                    "❌ Bạn chỉ có thể xóa các giao dịch mà bạn là chủ nợ!\n"
                    f"Giao dịch này thuộc về `{transaction['creditor_username'] or 'ID ' + str(transaction['creditor_id'])}`"
                )
                return False
            
            # Delete the transaction
            success = await database.delete_transaction(transaction_id, user_info['user_id'])
            
            if success:
                # Format deleted transaction info
                amount = format_money(abs(transaction['amount']))
                debtor_name = transaction['debtor_full_name'] or f"@{transaction['debtor_username']}"
                note_text = f" ({transaction['note']})" if transaction['note'] else ""
                
                confirm_text = f"""
✅ **Đã xóa giao dịch thành công!**

🗑️ **Thông tin giao dịch đã xóa:**
• ID: {transaction_id}
• Giao dịch: {debtor_name} nợ bạn {amount}{note_text}
• Thời gian: {transaction['created_at']}
                """.strip()
                
                await bot.send_message(
                    chat_info['chat_id'],
                    confirm_text
                )
                
                logger.info(f"Transaction deleted: ID {transaction_id} by user {user_info['username']}")
                return True
            else:
                await bot.send_message(
                    chat_info['chat_id'],
                    "❌ Đã có lỗi xảy ra khi xóa giao dịch. Vui lòng thử lại!"
                )
                return False
                
        except Exception as e:
            logger.error(f"Error handling /xoa: {e}")
            return False


# Dictionary mapping transaction commands to handlers
TRANSACTION_HANDLERS = {
    '/no': TransactionHandler.handle_no,
    '/tra': TransactionHandler.handle_tra,
    '/check': TransactionHandler.handle_check,
    '/xoa': TransactionHandler.handle_xoa,
}

async def handle_transaction_command(message: Dict) -> bool:
    """
    Route transaction command to appropriate handler
    
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
    handler = TRANSACTION_HANDLERS.get(command)
    if handler:
        return await handler(message)
    
    return False