import redis
import json

redis_client = None

def init_cache(app):
    global redis_client

    redis_client = redis.Redis.from_url(
        app.config["REDIS_URL"],
        decode_responses=True
    )

def get_cache(key):
    if not redis_client:
        return None

    data = redis_client.get(key)

    if data:
        return json.loads(data)

    return None

def set_cache(key, data, timeout=60):
    if redis_client:
        redis_client.set(
            key,
            json.dumps(data),
            ex=timeout
        )

def delete_cache(key):
    if redis_client:
        redis_client.delete(key)


def clear_cache_pattern(pattern):
    if redis_client:
        keys = redis_client.keys(pattern)

        if keys:
            redis_client.delete(*keys)

def clear_trek_cache():
    clear_cache_pattern("treks:*")
    clear_cache_pattern("trek:details:*")