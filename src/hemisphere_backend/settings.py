from pathlib import Path
from datetime import timedelta

import os, environ

env = environ.Env()

environ.Env.read_env()

# # aws credentials
# AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY')
# AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS')
# AWS_SECRET_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
# AWS_REGION_NAME = env('AWS_region')
# AWS_BUCKET_URL = env('AWS_bucket_url')

# # mapbox credentials
# MAPBOX_TOKEN = env('Mapbox_token')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-!8b!^srfuoe3p63tve3gm$-4q51_oyp8q1co&gyh6a0cvlg@p!"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["49.12.233.43", "localhost"]


# Application definition
AUTH_USER_MODEL = "users.ExtendedUser"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # installed apps
    "rest_framework",
    "corsheaders",
    "location_field.apps.DefaultConfig",
    # local apps
    "users",
    "surveys",
]

# LOCATION_FIELD = {
#     'provider.mapbox.access_token': MAPBOX_TOKEN,
#     'provider.mapbox.max_zoom': 13,
#     'provider.mapbox.id': 'mapbox.streets',
# }

# Rest Framework settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # declares the default authentication with rest_framework_simplejwt
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}

# declares the lifetime of the rest framework simple-jwt tokens
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=2),
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hemisphere_backend.urls"

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

WSGI_APPLICATION = "hemisphere_backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": "hemispheredb",
#         "USER": "hemisphereuser",
#         "HOST": "db",
#         "PORT": 5432,
#         "PASSWORD": "hemispheredb1234",
#     }
# }
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "hemispheredb",
        "USER": "hemisphereuser",
        "HOST": "hemisphere-back-db",
        "PORT": 5432,
        "PASSWORD": "hemispheredb1234",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOW_ALL_ORIGINS = True
