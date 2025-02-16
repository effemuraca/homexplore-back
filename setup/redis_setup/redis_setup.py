from os import environ
from redis.sentinel import Sentinel
from redis import exceptions
from config.config import settings

# Retrieve Sentinel hosts from environment variable.
sentinel_hosts_env = environ.get('SENTINEL_HOSTS')
if sentinel_hosts_env and sentinel_hosts_env.strip():
    sentinel_hosts = []
    for pair in sentinel_hosts_env.split(','):
        host, port = pair.split(':')
        sentinel_hosts.append((host.strip(), int(port.strip())))
else:
    sentinel_hosts = []
    temp_sentinel_hosts = settings.sentinel_hosts
    for pair in temp_sentinel_hosts.split(','):
        host, port = pair.split(':')
        sentinel_hosts.append((host.strip(), int(port.strip())))

MASTER_NAME = environ.get('REDIS_MASTER_NAME')
if MASTER_NAME is None or MASTER_NAME.strip() == '':
    MASTER_NAME = settings.redis_master_name

REDIS_DB = environ.get('REDIS_DB')
if REDIS_DB is None or REDIS_DB.strip() == '':
    REDIS_DB = settings.redis_db

sentinel = Sentinel(sentinel_hosts, socket_timeout=5.0)

redis_client = sentinel.master_for(MASTER_NAME, socket_timeout=1.0, db=int(REDIS_DB))

def get_redis_client():
    """
    Returns:
        redis.Redis: The Redis client instance connected to the current master.
    """
    return redis_client

def get_redis_keys(pattern: str = '*'):
    """
    Retrieves all Redis keys matching the specified pattern.

    Args:
        pattern (str): The pattern to match keys (default is '*').

    Returns:
        list: A list of keys matching the pattern.
    """
    return redis_client.keys(pattern)

RedisError = exceptions.RedisError
WatchError = exceptions.WatchError
