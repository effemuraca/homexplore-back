from os import environ
import redis
from redis import exceptions
from config.config import settings

REDIS_HOST = environ.get('REDIS_HOST')
REDIS_PORT = environ.get('REDIS_PORT')
REDIS_DB = environ.get('REDIS_DB')

if REDIS_HOST is None or REDIS_HOST == '':
    REDIS_HOST = settings.redis_host

if REDIS_PORT is None or REDIS_PORT == '':
    REDIS_PORT = settings.redis_port

if REDIS_DB is None or REDIS_DB == '':
    REDIS_DB = settings.redis_db

if REDIS_HOST is None or REDIS_PORT is None or REDIS_DB is None:
    raise Exception('Redis environment variables not set')

redis_client = redis.StrictRedis(host=REDIS_HOST, port=int(REDIS_PORT), db=int(REDIS_DB), decode_responses=True)

def get_redis_client():
    """
    This function returns the Redis client instance.
    """
    return redis_client

def get_redis_keys(pattern: str = '*'):
    """
    This function retrieves all keys matching a pattern in Redis.

    @param pattern: the pattern to match keys (default is '*').
    """
    return redis_client.keys(pattern)

RedisError = exceptions.RedisError
WatchError = exceptions.WatchError