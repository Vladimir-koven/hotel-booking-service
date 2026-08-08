from datetime import timedelta
from pathlib import Path

from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# === БЕЗОПАСНОСТЬ ===
SECRET_KEY = config("SECRET_KEY", default="django-insecure-dev-key-please-change-in-production")
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS: list[str] = config("ALLOWED_HOSTS", default="localhost,127.0.0.1").split(",")

# === БАЗА ДАННЫХ ===
DATABASE_URL = config("DATABASE_URL", default="sqlite:///db.sqlite3")

if DATABASE_URL.startswith("postgres"):
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}
    DATABASES["default"].update(
        {
            "CONN_MAX_AGE": 600,
            "OPTIONS": {
                "connect_timeout": 10,
            },
        }
    )
    print("PostgreSQL database configured")
elif DATABASE_URL.startswith("sqlite"):
    import re

    match = re.search(r"sqlite:///(.+)", DATABASE_URL)
    db_path = match.group(1) if match else "db.sqlite3"
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / db_path,
        }
    }
    print("SQLite database configured")
else:
    raise ValueError(f"Unsupported database URL: {DATABASE_URL}")

# === PRODUCTION CHECKS ===
if not DEBUG:
    if SECRET_KEY == "django-insecure-dev-key-please-change-in-production":
        raise ValueError("SECRET_KEY must be changed in production!")
    if "*" in ALLOWED_HOSTS:
        raise ValueError("ALLOWED_HOSTS cannot contain '*' in production!")

print(f"Application running in {'DEVELOPMENT' if DEBUG else 'PRODUCTION'} mode")

# === ПРИЛОЖЕНИЯ ===
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "apps.rooms.apps.RoomsConfig",
    "apps.bookings.apps.BookingsConfig",
    "apps.users.apps.UsersConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# === ВАЛИДАЦИЯ ПАРОЛЕЙ ===
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

# === ИНТЕРНАЦИОНАЛИЗАЦИЯ ===
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# === JWT ===
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# === DRF ===
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticatedOrReadOnly",),
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "EXCEPTION_HANDLER": "utils.exceptions.custom_exception_handler",
}

# === REDIS ===
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

try:
    import redis

    REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/1")
    redis_client = redis.from_url(REDIS_URL)
    redis_client.ping()

    CACHES["default"] = {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_CLASS": "redis.BlockingConnectionPool",
            "CONNECTION_POOL_CLASS_KWARGS": {
                "max_connections": 50,
                "timeout": 20,
            },
            "MAX_CONNECTIONS": 1000,
            "PICKLE_VERSION": 4,
            "SOCKET_TIMEOUT": 5,
            "SOCKET_CONNECT_TIMEOUT": 5,
            "RETRY_ON_TIMEOUT": True,
        },
        "KEY_PREFIX": "hotel",
        "TIMEOUT": 3600,
    }
    print("Redis cache enabled")
except Exception as e:
    print(f"Redis not available, using LocMemCache: {e}")
