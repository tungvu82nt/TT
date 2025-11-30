"""
Configuration management for SoNoBot
Loads environment variables and provides configuration settings
"""

import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for SoNoBot"""
    
    # SafeW Bot Configuration
    BOT_TOKEN: str = os.getenv('BOT_TOKEN', '')
    SAFEW_API_URL: str = "https://api.safew.org/bot"
    
    # Database Configuration
    DB_PATH: str = os.getenv('DB_PATH', 'sonobot.db')
    
    # Admin Configuration - Support multiple admin IDs (comma-separated)
    ADMIN_IDS: list = []
    if os.getenv('ADMIN_ID'):
        try:
            admin_ids_str = os.getenv('ADMIN_ID')
            # Support comma-separated admin IDs
            ADMIN_IDS = [int(admin_id.strip()) for admin_id in admin_ids_str.split(',') if admin_id.strip()]
        except ValueError:
            pass
    
    # Backward compatibility: single ADMIN_ID
    ADMIN_ID: Optional[int] = ADMIN_IDS[0] if ADMIN_IDS else None
    
    @classmethod
    def is_admin(cls, user_id: int) -> bool:
        """Check if user_id is an admin"""
        return user_id in cls.ADMIN_IDS
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # Bot Settings
    BOT_NAME: str = "SoNoBot"
    BOT_DESCRIPTION: str = "Bot quản lý nợ cá nhân và nhóm"
    
    # BigModel AI Configuration
    BIGMODEL_API_KEY: Optional[str] = os.getenv('BIGMODEL_API_KEY')
    BIGMODEL_API_URL: str = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    BIGMODEL_MODEL: str = "glm-4-flash"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        if not cls.BOT_TOKEN:
            print("❌ BOT_TOKEN is required!")
            return False
        # SafeW tokens don't start with ':', they use format: 123456789:abcdef...
        if ':' not in cls.BOT_TOKEN or len(cls.BOT_TOKEN) < 20:
            print("❌ Invalid BOT_TOKEN format!")
            print(f"Token: {cls.BOT_TOKEN[:10]}...")
            return False
        return True
    
    @classmethod
    def get_api_url(cls, method: str) -> str:
        """Get SafeW API URL for specific method"""
        return f"{cls.SAFEW_API_URL}{cls.BOT_TOKEN}/{method}"


# Create global config instance
config = Config()

# Note: Validation is done when bot starts, not on import
# This allows importing config without requiring .env file immediately