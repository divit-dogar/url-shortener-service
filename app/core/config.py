from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    
    # Application Settings
    
    APP_NAME: str
    APP_ENV: str
    DEBUG: bool

   
    # Database
   
    DATABASE_URL: str

   
    # JWT Authentication
    
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

   
    # Pydantic Configuration
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()