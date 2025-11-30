"""
BigModel AI Integration for SoNoBot
Integrates GLM-4-flash model for intelligent responses
"""

import aiohttp
import json
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class BigModelAI:
    """BigModel AI integration class"""
    
    def __init__(self, api_key: str, api_url: str = None):
        self.api_key = api_key
        self.api_url = api_url or "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        self.model = "glm-4-flash"
        
    async def chat_completion(self, messages: list, **kwargs) -> Optional[str]:
        """
        Send chat completion request to BigModel API
        
        Args:
            messages: List of message dictionaries with role and content
            **kwargs: Additional parameters for the API
            
        Returns:
            AI response text or None if error
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1000,
                **kwargs
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        if result.get('choices') and len(result['choices']) > 0:
                            return result['choices'][0]['message']['content']
                        else:
                            logger.error(f"Unexpected API response: {result}")
                            return None
                    else:
                        error_text = await response.text()
                        logger.error(f"BigModel API error {response.status}: {error_text}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error calling BigModel API: {e}")
            return None
    
    async def get_help_response(self, user_question: str = None) -> str:
        """
        Generate help response with AI context
        
        Args:
            user_question: Optional user question to provide more specific help
            
        Returns:
            Formatted help text with AI insights
        """
        base_help = """
🤖 **SoNoBot AI Assistant** - Hỗ trợ quản lý nợ thông minh

💰 **Tính năng chính:**
• Quản lý nợ cá nhân và nhóm
• Parser tiền tệ thông minh (50k, 1.5tr, 1000)
• Lịch sử giao dịch chi tiết
• AI Assistant trả lời câu hỏi

📝 **Cách sử dụng:**
• `+10` → NẠP 10,000đ
• `-50k` → RÚT 50,000đ  
• `+100k cafe` → NẠP 100,000đ (ghi chú: cafe)
• `100k trưa` → NẠP 100,000đ (ghi chú: trưa)

🧠 **AI Assistant:**
• Hỏi bất kỳ câu hỏi nào về quản lý tài chính
• Tính toán phức tạp
• Gợi ý quản lý nợ hiệu quả

💡 **Mẹo:** Bắt đầu bằng `/help` để xem hướng dẫn chi tiết!
        """
        
        if not user_question:
            return base_help
            
        # If user asked a question, provide contextual help
        messages = [
            {
                "role": "system", 
                "content": "Bạn là AI assistant của SoNoBot - bot quản lý nợ cá nhân và nhóm. Hãy trả lời câu hỏi một cách hữu ích và thực tế."
            },
            {
                "role": "user", 
                "content": f"Câu hỏi: {user_question}\n\nCung cấp hướng dẫn cụ thể về tính năng của SoNoBot."
            }
        ]
        
        ai_response = await self.chat_completion(messages)
        if ai_response:
            return f"🤖 **AI Assistant trả lời:**\n\n{ai_response}"
        else:
            return base_help
    
    async def analyze_transaction(self, transaction_text: str) -> str:
        """
        Analyze transaction with AI insights
        
        Args:
            transaction_text: The transaction to analyze
            
        Returns:
            AI analysis and suggestions
        """
        messages = [
            {
                "role": "system",
                "content": "Bạn là chuyên gia tư vấn tài chính. Phân tích giao dịch và đưa ra lời khuyên hữu ích."
            },
            {
                "role": "user",
                "content": f"Giao dịch: {transaction_text}\nHãy phân tích và đưa ra lời khuyên quản lý tài chính cá nhân."
            }
        ]
        
        ai_response = await self.chat_completion(messages)
        if ai_response:
            return f"💡 **AI Phân tích:**\n\n{ai_response}"
        return "Xin lỗi, AI暂时无法分析 giao dịch này."