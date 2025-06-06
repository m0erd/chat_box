from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv
from datetime import timedelta


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', "backend-production-bea1.up.railway.app"]

# Application definition

INSTALLED_APPS = [
    "chat",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "channels",
    "rest_framework",
    "rest_framework_simplejwt",
    "users",
    "core",
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
]

ASGI_APPLICATION = 'chatapp.asgi.application'

REDIS_HOST = os.environ.get("REDISHOST", "127.0.0.1")
REDIS_PORT = os.environ.get("REDISPORT", "6379")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")

REDIS_PORT = int(REDIS_PORT) if REDIS_PORT else 6379

if REDIS_PASSWORD:
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"
else:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
    },
}
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [{
#                 "address": "redis://127.0.0.1:6379",
#                 "retry_policy": {
#                     "max_retries": 5,
#                     "interval_start": 0.1,
#                     "interval_step": 0.5,
#                     "interval_max": 2.0,
#                 }
#             }],
#         },
#     },
# }


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = "chatapp.urls"

# TEMPLATES = [
#     {
#         "BACKEND": "django.template.backends.django.DjangoTemplates",
#         "DIRS": [
#             os.path.join(BASE_DIR, "frontend/build"),
#         ],
#         "APP_DIRS": True,
#         "OPTIONS": {
#             "context_processors": [
#                 "django.template.context_processors.request",
#                 "django.contrib.auth.context_processors.auth",
#                 "django.contrib.messages.context_processors.messages",
#             ],
#         },
#     },
# ]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'frontend/build')
        ],
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

WSGI_APPLICATION = "chatapp.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

AUTH_USER_MODEL = 'users.CustomUser'

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# LOG_LEVEL = 'INFO'  # or WARNING / ERROR in prod
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name} - {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} - {message}',
            'style': '{',
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'chat_file': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/chat.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5MB
            'backupCount': 3,
            'formatter': 'verbose',
        },
        'users_file': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/users.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 3,
            'formatter': 'verbose',
        },
        'django_file': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 3,
            'formatter': 'verbose',
        },
    },

    'root': {
        'handlers': ['console'],
        'level': LOG_LEVEL,
    },

    'loggers': {
        'django': {
            'handlers': ['console', 'django_file'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'users': {
            'handlers': ['console', 'users_file'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'chat': {
            'handlers': ['console', 'chat_file'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
    },
}

# STATICFILES_DIRS = [
#     os.path.join('frontend/build/static'),
# ]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://backend-production-bea1.up.railway.app/",
    "https://frontend-production-7a9d.up.railway.app/",
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
