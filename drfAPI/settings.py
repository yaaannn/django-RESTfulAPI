from pathlib import Path, PurePath
from datetime import timedelta
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# config path
CONFIG_PATH = PurePath.joinpath(BASE_DIR, 'config')

# set env 
CURRENT_ENV = os.getenv('ENV', 'dev')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-u1spo7h^t0i=h&k9ixv(^p)1&xege7al#rsuf!u8g2t=1z3i97'
INTERFACE_KEY = '16ed9ecc7d9011eab9c63c6aa7c68b67'
INTERFACE_TIMEOUT = 60
DISPATCH_KEYS = ('admin4b67e4c11eab49a3c6aa7c68b67', 'mobile347e4c11eab49a3c6aa7c68b67', 'mini235a7e4c11eab49a3c6aa7c68b67')

# 配置请求体大小100m 处理跨域的问题
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 64
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS= True
CORS_ALLOW_HEADERS = [
    '*',
]
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'drf_yasg',
    'debug_toolbar',
]

# set middeware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # 解决跨域中间件
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware', # debug 中间件
]

# set default urls
ROOT_URLCONF = 'drfAPI.urls'

# set template
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

# set wsgi app
WSGI_APPLICATION = 'drfAPI.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    # 指定文件目录，BASE_DIR指的是项目目录，static是指存放静态文件的目录。
    PurePath.joinpath(BASE_DIR, 'static'),
]
# 迁移静态文件的目录,这个是线上是需要使用的 python manage.py collectstatic
STATIC_ROOT = PurePath.joinpath(BASE_DIR, 'static/static')

# 媒体文件位置
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# rest 相关配置
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        # 'drf_renderer_xlsx.renderers.XLSXRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    # 格式化时间
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATETIME_INPUT_FORMATS': ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M'),
    'DATE_FORMAT': '%Y-%m-%d',
    'DATE_INPUT_FORMATS': ('%Y-%m-%d',),
    'TIME_FORMAT': '%H:%M:%S',
    'TIME_INPUT_FORMATS': ('%H:%M:%S',),
    # DRF异常定制处理方法
    'EXCEPTION_HANDLER': 'common.exceptionHandle.base_exception_handler',
    # DRF返回response定制json
    'DEFAULT_RENDERER_CLASSES': (
        'common.rendererresponse.BaseJsonRenderer',
    ),
}

# set file type
FILE_CHECK = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'zip', 'rar', 'xls', 'xlsx', 'doc', 'docx', 'pptx', 'ppt', 'txt', 'pdf']
UPLOAD_DIR = PurePath.joinpath(PurePath.joinpath(BASE_DIR, 'media'), 'upload')

# set cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "SERIALIZER": "django_redis.serializers.msgpack.MSGPackSerializer",
            #"PASSWORD": ""
        }
    },
    "cache_redis": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# set jwt token
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# set swagger
SWAGGER_SETTINGS = {
    # 使用这个时需要使用django-rest的admin 也就是需要配置 url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # 'LOGIN_URL': 'rest_framework:login',
    # 'LOGOUT_URL': 'rest_framework:logout',
    # 自定义swagger的路由tag
    'DEFAULT_GENERATOR_CLASS': 'config.swagger.BaseOpenAPISchemaGenerator',
    'USE_SESSION_AUTH': False,
    # 'SHOW_EXTENSIONS': False,
    'DOC_EXPANSION': 'none',
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

if CURRENT_ENV == 'dev':
    # set server name
    SERVER_NAME = '127.0.0.1'
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    ALLOWED_HOSTS = ['*', ]
    # Database
    # https://docs.djangoproject.com/en/3.2/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # set server name
    SERVER_NAME = 'www.line.com'
    # set ssl header
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False
    ALLOWED_HOSTS = [
        '127.0.0.1',
    ]
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'drfAPI',
            'USER': 'root',
            'PASSWORD': '123456',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'OPTIONS': {
                "init_command": "SET foreign_key_checks = 0;",  # 去除强制外键约束
                'charset': 'utf8mb4',
                'sql_mode': 'traditional'
            }
        }
    }
    '''
    sql_mode
    ANSI：宽松模式，对插入数据进行校验，如果不符合定义类型或长度，对数据类型调整或截断保存，报warning警告。
    TRADITIONAL：严格模式，当向mysql数据库插入数据时，进行数据的严格校验，保证错误数据不能插入，报error错误。用于事物时，会进行事物的回滚。
    STRICT_TRANS_TABLES：严格模式，进行数据的严格校验，错误数据不能插入，报error错误。
    '''

# 日志配置
LOGGING = {
    'version': 1,  # 指明dictConnfig的版本
    'disable_existing_loggers': False,  # 表示是否禁用所有的已经存在的日志配置
    'formatters': {  # 格式器
        'verbose': {  # 详细
            'format': '[%(levelname)s] %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'standard': {  # 标准
            'format': '[%(asctime)s] %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
        },
        "debug": { # 调试
            "format": "[%(asctime)s] [%(process)d:%(thread)d] %(filename)s[line:%(lineno)d] (%(name)s)[%(levelname)s] %(message)s",
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',  # 当开启调试模式时使用debug模式，否则使用info模式
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'standard'
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        "debug_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "debug",
            "level": "DEBUG",
            "encoding": "utf8",
            "filename": "./logs/debug.log",
            "mode": "w"
        },
        "info_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "level": "INFO",
            "encoding": "utf8",
            "filename": "./logs/info.log",
            "mode": "w"
        },
        "error_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "debug",
            "level": "ERROR",
            "encoding": "utf8",
            "filename": "./logs/error.log",
            "mode": "w"
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['null'],
            'level': 'INFO',
            'propagate': False,
        },
        # 用于关闭django默认的request日志 必要时可开启
        # 'django.request': {
        #     'handlers': ['null'],
        #     'level': 'INFO',
        #     'propagate': False,
        # },
    },
    # 设置默认的root handle 用于将开发手动输出的日志输出到指定文件中
    'root': {
        'level': 'DEBUG',
        'handlers': ['debug_file_handler', 'info_file_handler', 'error_file_handler']
    }
}