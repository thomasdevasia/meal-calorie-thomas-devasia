import redis
import json
from app.config import Settings


def get_redis_client():
    settings = Settings()
    redis_url = settings.redis_url
    return redis.from_url(redis_url, encoding="utf-8", decode_responses=True)

def get_cached_item(key: str):
    try:
        redis_client = get_redis_client()
        cached_data = redis_client.get(key)
        if cached_data:
            return json.loads(cached_data) # type: ignore
        return None
    except Exception as e:
        print(f"Error retrieving from cache: {e}")
        return None
    
def set_cached_item(key: str, value: dict, expire_seconds: int = 3600):
    try:
        redis_client = get_redis_client()
        redis_client.set(key, json.dumps(value), ex=expire_seconds)
        return True
    except Exception as e:
        print(f"Error setting cache: {e}")
        return False