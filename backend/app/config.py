from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    database_url: str = "mysql+pymysql://root:password@localhost:3306/spectrum_insight"
    redis_url: str = "redis://localhost:6379/0"
    upload_dir: str = "./uploads"
    max_upload_size_mb: int = 100
    ai_inference_url: str = "http://localhost:8501"
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
