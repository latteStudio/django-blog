from .common import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'development-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['*']
HAYSTACK_CONNECTIONS['default']['URL'] = 'http://elasticsearch-dev:9200'
# 在容器的环境变量，自动解析为依赖的es容器的ip
