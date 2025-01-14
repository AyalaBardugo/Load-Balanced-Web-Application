"""Configuration settings for database connections and logging system"""
import os
import logging

class Config:
    """Database configuration using environment variables with defaults"""
    DB_HOST = os.getenv("DB_HOST", "mysql-db")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "rootpassword")
    DB_NAME = os.getenv("DB_NAME", "app_db")

class LogConfig:
    """Logging system configuration and initialization"""
    LOG_DIR = "/app/logs"
    LOG_FILE = os.path.join(LOG_DIR, "app.log")
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(funcName)s() - %(message)s"
    LOG_LEVEL = "DEBUG"
    
    @classmethod
    def setup_logging(cls) -> None:
        """Initialize logging configuration"""
        os.makedirs(cls.LOG_DIR, exist_ok=True)
        
        logging.basicConfig(
            filename=cls.LOG_FILE,
            level=getattr(logging, cls.LOG_LEVEL),
            format=cls.LOG_FORMAT
        )
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(cls.LOG_FORMAT))
        logging.getLogger('').addHandler(console_handler)
    