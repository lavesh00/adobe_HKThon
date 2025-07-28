import platform
from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    Defines the configuration settings for the application.
    Settings can be overridden by environment variables or a .env file.
    """
    MAX_PDF_PROCESS_TIME: int = 10  # seconds
    MAX_MULTI_PROCESS_TIME: int = 60  # seconds
    MODEL_SIZE_LIMIT_MB: int = 1000
    DEBUG_MODE: bool = False
    OS: str = platform.system()

    class Config:
        env_file = ".env"

# Create a single, importable instance of the settings
settings = Settings()
