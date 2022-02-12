from .common import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ["192.168.80.200"]
HAYSTACK_CONNECTIONS['default']['URL'] = 'http://elasticsearch-prod:9200'


CACHES = {
    'default': {
        'BACKEND': 'redis_cache_RedisCache',
        'LOCATION': 'redis://:UJaoRZlNrH40BDaWU6fi@redis:6379/0',
        'OPTIONS': {
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnetionPool',
            'CONNECTION_POLL_CLASS_KWARGS': {'max_connections': 50, 'timeout': 20},
            'MAX_CONNECTIONS': 1000,
            'PICKLE_VERSION': -1,
        }
    }
}