"""
SafeW Bot implementation for SoNoBot
Handles communication with SafeW API
"""

import aiohttp
import asyncio
import logging
from typing import Dict, Optional, List, Any
from .config import config

# Configure logging
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class SafeWBot:
    """SafeW Bot client implementation"""
    
    def __init__(self):
        self.token = config.BOT_TOKEN
        self.api_url = config.SAFEW_API_URL
        self.session = None
        self.offset = 0
        self.timeout = 30
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def start(self):
        """Start the bot session"""
        if self.session is None:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self.session = aiohttp.ClientSession(timeout=timeout)
        
        # Verify bot token by getting bot info
        bot_info = await self.get_me()
        if bot_info and bot_info.get('ok'):
            logger.info(f"Bot started: {bot_info['result']['username']}")
        else:
            raise ValueError("Invalid bot token or failed to connect to SafeW API")
    
    async def close(self):
        """Close the bot session"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def _make_request(self, method: str, data: Dict[str, Any] = None, files: Dict = None) -> Optional[Dict]:
        """
        Make HTTP request to SafeW API
        
        Args:
            method: SafeW API method name
            data: POST data
            files: Files to upload
            
        Returns:
            JSON response or None if error
        """
        if not self.session:
            await self.start()
        
        url = f"{self.api_url}{self.token}/{method}"
        
        try:
            if files:
                # Handle file uploads
                data = aiohttp.FormData()
                for key, value in files.items():
                    data.add_field(key, value)
                
                response = await self.session.post(url, data=data)
            elif data:
                response = await self.session.post(url, json=data)
            else:
                response = await self.session.get(url)
            
            if response.status == 200:
                return await response.json()
            else:
                error_text = await response.text()
                logger.error(f"API request failed: {response.status} - {error_text}")
                return None
                
        except aiohttp.ClientError as e:
            logger.error(f"Network error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
    
    # Bot info methods
    async def get_me(self) -> Optional[Dict]:
        """Get bot information"""
        return await self._make_request('getMe')
    
    async def get_updates(self, timeout: int = 30, allowed_updates: List[str] = None) -> Optional[Dict]:
        """Get bot updates (messages, etc.)"""
        data = {
            'timeout': timeout,
            'offset': self.offset,
            'allowed_updates': allowed_updates or ['message', 'callback_query']
        }
        result = await self._make_request('getUpdates', data)
        
        if result and result.get('ok'):
            updates = result.get('result', [])
            if updates:
                # Update offset to avoid receiving the same updates
                self.offset = updates[-1]['update_id'] + 1
            
        return result
    
    # Message sending methods
    async def send_message(self, chat_id: int, text: str, parse_mode: str = None, 
                          reply_to_message_id: int = None, reply_markup: Dict = None) -> Optional[Dict]:
        """Send text message"""
        data = {
            'chat_id': chat_id,
            'text': text
        }
        
        if parse_mode:
            data['parse_mode'] = parse_mode
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            data['reply_markup'] = reply_markup
            
        return await self._make_request('sendMessage', data)
    
    async def send_photo(self, chat_id: int, photo: str, caption: str = None, 
                        reply_to_message_id: int = None, reply_markup: Dict = None) -> Optional[Dict]:
        """Send photo"""
        data = {
            'chat_id': chat_id,
            'photo': photo
        }
        
        if caption:
            data['caption'] = caption
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            data['reply_markup'] = reply_markup
            
        return await self._make_request('sendPhoto', data)
    
    async def send_document(self, chat_id: int, document: str, caption: str = None,
                           reply_to_message_id: int = None, reply_markup: Dict = None) -> Optional[Dict]:
        """Send document"""
        data = {
            'chat_id': chat_id,
            'document': document
        }
        
        if caption:
            data['caption'] = caption
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            data['reply_markup'] = reply_markup
            
        return await self._make_request('sendDocument', data)
    
    # Message editing methods
    async def edit_message_text(self, chat_id: int, message_id: int, text: str,
                               parse_mode: str = None, reply_markup: Dict = None) -> Optional[Dict]:
        """Edit message text"""
        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': text
        }
        
        if parse_mode:
            data['parse_mode'] = parse_mode
        if reply_markup:
            data['reply_markup'] = reply_markup
            
        return await self._make_request('editMessageText', data)
    
    async def edit_message_reply_markup(self, chat_id: int, message_id: int,
                                       reply_markup: Dict = None) -> Optional[Dict]:
        """Edit message reply markup"""
        data = {
            'chat_id': chat_id,
            'message_id': message_id
        }
        
        if reply_markup:
            data['reply_markup'] = reply_markup
            
        return await self._make_request('editMessageReplyMarkup', data)
    
    # Message deletion methods
    async def delete_message(self, chat_id: int, message_id: int) -> Optional[Dict]:
        """Delete a message"""
        data = {
            'chat_id': chat_id,
            'message_id': message_id
        }
        return await self._make_request('deleteMessage', data)
    
    # Chat methods
    async def get_chat(self, chat_id: int) -> Optional[Dict]:
        """Get chat information"""
        data = {'chat_id': chat_id}
        return await self._make_request('getChat', data)
    
    async def get_chat_member(self, chat_id: int, user_id: int) -> Optional[Dict]:
        """Get chat member information"""
        data = {
            'chat_id': chat_id,
            'user_id': user_id
        }
        return await self._make_request('getChatMember', data)
    
    async def get_chat_administrators(self, chat_id: int) -> Optional[Dict]:
        """Get chat administrators"""
        data = {'chat_id': chat_id}
        return await self._make_request('getChatAdministrators', data)
    
    async def get_chat_member_count(self, chat_id: int) -> Optional[Dict]:
        """Get chat member count"""
        data = {'chat_id': chat_id}
        return await self._make_request('getChatMemberCount', data)
    
    # Bot command methods
    async def get_my_commands(self) -> Optional[Dict]:
        """Get bot commands"""
        return await self._make_request('getMyCommands')
    
    async def set_my_commands(self, commands: List[Dict]) -> Optional[Dict]:
        """Set bot commands"""
        data = {'commands': commands}
        return await self._make_request('setMyCommands', data)
    
    # Callback query methods
    async def answer_callback_query(self, callback_query_id: str, text: str = None,
                                   show_alert: bool = False, url: str = None,
                                   cache_time: int = 0) -> Optional[Dict]:
        """Answer callback query"""
        data = {'callback_query_id': callback_query_id}
        
        if text:
            data['text'] = text
        if show_alert:
            data['show_alert'] = show_alert
        if url:
            data['url'] = url
        if cache_time:
            data['cache_time'] = cache_time
            
        return await self._make_request('answerCallbackQuery', data)
    
    # Utility methods
    def extract_user_info(self, message: Dict) -> Optional[Dict]:
        """Extract user information from message"""
        if not message or 'from' not in message:
            return None
            
        user = message['from']
        return {
            'user_id': user.get('id'),
            'username': user.get('username'),
            'full_name': f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
        }
    
    def extract_chat_info(self, message: Dict) -> Optional[Dict]:
        """Extract chat information from message"""
        if not message or 'chat' not in message:
            return None
            
        chat = message['chat']
        return {
            'chat_id': chat.get('id'),
            'chat_type': chat.get('type'),
            'chat_title': chat.get('title')
        }
    
    def extract_text_content(self, message: Dict) -> Optional[str]:
        """Extract text content from message"""
        if not message:
            return None
            
        return message.get('text') or message.get('caption') or ''
    
    def parse_command(self, text: str) -> Optional[tuple]:
        """Parse command from message text"""
        if not text or not text.startswith('/'):
            return None
            
        parts = text.split(maxsplit=1)
        command = parts[0].lower()
        
        # Extract command without @botname
        command = command.split('@')[0]
        
        args = parts[1] if len(parts) > 1 else ''
        
        return command, args


# Global bot instance
bot = SafeWBot()