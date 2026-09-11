from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
import redis.asyncio as aioredis

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

redis_client: aioredis.Redis | None = None


async def init_db():
    global redis_client
    try:
        redis_client = aioredis.from_url(settings.redis_url, decode_responses=True)
        await redis_client.ping()
        print(f"[Redis] Connected to {settings.redis_url}")
    except Exception as e:
        print(f"[Redis] Connection failed ({e}), running without Redis cache")
        redis_client = None
    Base.metadata.create_all(bind=engine)
    print(f"[DB] Database initialized: {settings.database_url}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_redis():
    return redis_client
