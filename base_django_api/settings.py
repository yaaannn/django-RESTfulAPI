import os
import datetime
import pymysql
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 如果使用apps管理应用
# sys.path.insert(0, BASE_DIR)
# sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0b($)a_$n$!grvsj!pob$5z4(q+u3fo_)aoz!g)3^=pk@7g770'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  #开发时设置为True 线上环境设置为False

ALLOWED_HOSTS = ['*']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

# 配置请求体大小100m
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600

# 处理跨域的问题
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS= True
CORS_ALLOW_HEADERS = ('*')

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'base.apps.BaseConfig',
    'django_crontab',
    'django_filters',
    'drf_yasg',
    # 'rest_framework_jwt'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 跨域新增的中间件
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.BaseMiddleWare.myMiddle',   # 日志格式化中间件
    'middleware.BaseMiddleWare.JsondataMiddleware',   # response 格式化中间件
]

ROOT_URLCONF = 'base_django_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'base_django_api.wsgi.application'


# Database
# 使用测试 sqlite3 数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''
# 使用mysql数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'douban-zufang',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
'''

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'zh-hans'  #中文语言

TIME_ZONE = 'Asia/Shanghai'  #中文时区

USE_I18N = True

USE_L10N = True

USE_TZ = False  #不使用UTC格式时间


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    # 指定文件目录，BASE_DIR指的是项目目录，static是指存放静态文件的目录。
    os.path.join(BASE_DIR , 'static'),
]
# 迁移静态文件的目录,这个是线上是需要使用的 python manage.py collectstatic
STATIC_ROOT = os.path.join(BASE_DIR , 'static/static')

# 媒体文件位置
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# rest 相关配置
# REST_FRAMEWORK = {
    # 'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    # # 权限认证
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),
    # # 身份验证
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    #     'rest_framework.authentication.SessionAuthentication',
    #     'rest_framework.authentication.BasicAuthentication',
    # ),
# }

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SERIALIZER": "django_redis.serializers.msgpack.MSGPackSerializer",
            #"PASSWORD": ""
        }
    }
}

'''
# Aliyun OSS
ACCESS_KEY_ID = "LTAI6hxpAQNHm0hE"
ACCESS_KEY_SECRET = "Iw7jlRBsutGR2PUgg0vnydRzXETCOX"
END_POINT = "oss-cn-hangzhou.aliyuncs.com"
BUCKET_NAME = "beatop-h5"
ALIYUN_OSS_CNAME = ""  # 自定义域名，如果不需要可以不填写
BUCKET_ACL_TYPE = "public-read"  # private, public-read, public-read-write
# mediafile将自动上传
DEFAULT_FILE_STORAGE = 'aliyun_oss2_storage.backends.AliyunMediaStorage'
# staticfile将自动上传
#STATICFILES_STORAGE = 'aliyun_oss2_storage.backends.AliyunStaticStorage'
'''

SWAGGER_SETTINGS = {
    # 使用这个时需要使用django默认自带的admin
    # 'LOGIN_URL': '/admin/login',
    # 'LOGOUT_URL': '/admin/logout',
    # 使用这个时需要使用django-rest的admin 也就是需要配置 url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # 'LOGIN_URL': 'rest_framework:login',
    # 'LOGOUT_URL': 'rest_framework:logout',
    # 'DEFAULT_INFO': 'beatop.urls.swagger_info',
    'USE_SESSION_AUTH': False, # 不使用django自带的admin登录
    # 'SHOW_EXTENSIONS': False,
    'DOC_EXPANSION': 'none',  # none/list/full
    'SECURITY_DEFINITIONS': {
        # 'Basic': {
        #     'type': 'basic'
        # },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

# 定时任务
'''
crontab范例：
每五分钟执行    */5 * * * *
每小时执行     0 * * * *
每天执行       0 0 * * *
每周执行       0 0 * * 0
每月执行       0 0 1 * *
'''
CRONJOBS = [
    # 表示每一分钟执行一次
    ('*/1 * * * *', 'base.utils.task','>> /tmp/testapi_crontab.log') # 必须存在这个log文件
]


# JWT 使用官方jwt时开启此配置
# JWT_AUTH = {
#     'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
#     'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
#     'JWT_AUTH_HEADER_PREFIX': 'Bearer ',
# }

# 日志配置
LOGGING = {
    'version': 1,  # 指明dictConnfig的版本
    'disable_existing_loggers': False,  # 表示是否禁用所有的已经存在的日志配置
    'formatters': {  # 格式器
        'verbose': {  # 详细
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'standard': {  # 标准
            'format': '[%(asctime)s] [%(levelname)s] %(message)s'
        },
    },
    'handlers': { 
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout', 
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}