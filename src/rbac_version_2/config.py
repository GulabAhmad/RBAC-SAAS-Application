from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    database_url: str = "postgresql://user:password@localhost/rbac_db"
    
    # JWT settings
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Email settings
    email_address: str = "gulabahmad724@gmail.com"
    email_password: str = "xoqdnmyentuyqwzx"
    email_smtp_server: str = "smtp.gmail.com"
    email_smtp_port: int = 465
    
    # Application settings
    app_name: str = "RBAC System"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
