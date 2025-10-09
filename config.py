import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Bot Configuration
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    _admin_chat_id = os.getenv('ADMIN_CHAT_ID', '0')
    try:
        ADMIN_CHAT_ID = int(_admin_chat_id)
    except ValueError:
        # If it's a username, set to 0 and let the bot handle it
        ADMIN_CHAT_ID = 0
        ADMIN_USERNAME_TELEGRAM = _admin_chat_id
    
    # OpenRouter API Configuration
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', 'openai/gpt-3.5-turbo')
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    
    # Payment Configuration
    TON_WALLET_ADDRESS = os.getenv('TON_WALLET_ADDRESS')
    TELEGRAM_STARS_ENABLED = os.getenv('TELEGRAM_STARS_ENABLED', 'true').lower() == 'true'
    TON_ENABLED = os.getenv('TON_ENABLED', 'true').lower() == 'true'
    
    # Admin Dashboard Configuration
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DASHBOARD_HOST = os.getenv('DASHBOARD_HOST', '127.0.0.1')
    DASHBOARD_PORT = int(os.getenv('DASHBOARD_PORT', 5000))
    
    # Database Configuration
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'bot_database.db')
    
    # Bot Settings
    SIMULATION_MODE = os.getenv('SIMULATION_MODE', 'false').lower() == 'true'
    BOT_RUNNING = os.getenv('BOT_RUNNING', 'true').lower() == 'true'
    FREE_MESSAGES = int(os.getenv('FREE_MESSAGES', 1))
    
    # Default Pricing
    DEFAULT_TEXT_PRICE = int(os.getenv('DEFAULT_TEXT_PRICE', 1))
    DEFAULT_IMAGE_PRICE = int(os.getenv('DEFAULT_IMAGE_PRICE', 2))
    DEFAULT_VIDEO_PRICE = int(os.getenv('DEFAULT_VIDEO_PRICE', 3))
    
    # Advanced Settings
    MAX_IMAGE_SIZE = int(os.getenv('MAX_IMAGE_SIZE', 10))  # MB
    MAX_VIDEO_SIZE = int(os.getenv('MAX_VIDEO_SIZE', 50))  # MB
    AI_RESPONSE_TIMEOUT = int(os.getenv('AI_RESPONSE_TIMEOUT', 30))  # seconds
    
    # Webhook Configuration
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    WEBHOOK_PATH = os.getenv('WEBHOOK_PATH', '/webhook')
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE = int(os.getenv('MAX_REQUESTS_PER_MINUTE', 20))
    MAX_REQUESTS_PER_HOUR = int(os.getenv('MAX_REQUESTS_PER_HOUR', 100))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        required_vars = ['BOT_TOKEN', 'OPENROUTER_API_KEY']
        missing_vars = []
        
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True
    
    @classmethod
    def get_all_settings(cls):
        """Get all configuration settings as a dictionary"""
        return {
            'bot_token': cls.BOT_TOKEN,
            'admin_chat_id': cls.ADMIN_CHAT_ID,
            'openrouter_api_key': cls.OPENROUTER_API_KEY,
            'openrouter_model': cls.OPENROUTER_MODEL,
            'ton_wallet_address': cls.TON_WALLET_ADDRESS,
            'telegram_stars_enabled': cls.TELEGRAM_STARS_ENABLED,
            'ton_enabled': cls.TON_ENABLED,
            'simulation_mode': cls.SIMULATION_MODE,
            'bot_running': cls.BOT_RUNNING,
            'free_messages': cls.FREE_MESSAGES,
            'max_image_size': cls.MAX_IMAGE_SIZE,
            'max_video_size': cls.MAX_VIDEO_SIZE,
            'ai_response_timeout': cls.AI_RESPONSE_TIMEOUT,
            'webhook_url': cls.WEBHOOK_URL,
            'max_requests_per_minute': cls.MAX_REQUESTS_PER_MINUTE,
            'max_requests_per_hour': cls.MAX_REQUESTS_PER_HOUR,
            'log_level': cls.LOG_LEVEL
        }
    
    @classmethod
    def update_setting(cls, key: str, value: str):
        """Update a configuration setting"""
        # This could write back to .env file or database
        # For now, just update the class attribute
        if hasattr(cls, key.upper()):
            setattr(cls, key.upper(), value)
    
    @classmethod
    def reload_config(cls):
        """Reload configuration from environment"""
        load_dotenv(override=True)
        # Re-initialize all class variables
        cls.__init_subclass__()
    
    @classmethod
    def is_production(cls):
        """Check if running in production mode"""
        return not cls.SIMULATION_MODE
    
    @classmethod
    def get_ai_models(cls):
        """Get list of available AI models"""
        return [
            'openai/gpt-3.5-turbo',
            'openai/gpt-4',
            'anthropic/claude-3-haiku',
            'anthropic/claude-3-sonnet',
            'google/gemini-pro',
            'mistralai/mistral-7b-instruct'
        ]