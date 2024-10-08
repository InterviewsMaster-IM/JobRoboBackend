"""
Django settings for JobRoboBackend project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-8=!ds1)(^$*jw645^#j!l+^crzgr-tnn4@oflf(j48u^l@oelz"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "jobrobo.ai", "www.jobrobo.ai",
                 "3.142.79.103", "18.218.180.246", "3.145.41.95"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Installed apps
    "rest_framework_simplejwt",
    "storages",
    "corsheaders",
    "rest_framework",
    "drf_yasg",
    # Our apps
    "authentication",
    "resumes",
    "referrals",
    "credits",
    "profiles",
    "campaigns",
    "landing_pages",
    "logger",
    "Jobs",
    "robos",
]

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

ROOT_URLCONF = "JobRoboBackend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR/'landing_pages'/'templates'],
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

WSGI_APPLICATION = "JobRoboBackend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Settings for linkedin auth (our custom oauth flow)

LINKEDIN_AUTHORIZATION_URL = 'https://www.linkedin.com/oauth/v2/authorization'
LINKEDIN_ACCESS_TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
LINKEDIN_CLIENT_ID = '77lt6h9k4vxtes'
LINKEDIN_CLIENT_SECRET = 'ndfVcXhLLKIvggEf'

# LINKEDIN_REDIRECT_URI = 'http://localhost:8000/authentication/linkedin/callback'
LINKEDIN_REDIRECT_URI = 'http://jobrobo.ai/authentication/linkedin/callback'

LINKEDIN_SCOPE = 'openid profile email'  # Modify as per your requirements


# GOOGLE OAUTH Settings

# GOOGLE_CLIENT_ID = '724831200210-ji9err86cc5ndsetbhmhv5ekkf3gruj7.apps.googleusercontent.com'
# GOOGLE_CLIENT_ID = '239956764777-3bhalmfisn9997ih1jofq6fptpphlrit.apps.googleusercontent.com'
GOOGLE_CLIENT_ID = '945452418848-rrslmlqbtrc8u4ls34kj41qm4sdcjj7b.apps.googleusercontent.com'


# GOOGLE_CLIENT_SECRET = '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'
# GOOGLE_CLIENT_SECRET = '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'
GOOGLE_CLIENT_SECRET = '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'


# GOOGLE_REDIRECT_URI = 'https://jobrobo.ai/authentication/google/callback'
GOOGLE_REDIRECT_URI = 'http://localhost:8000/authentication/google/callback'

GOOGLE_AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_ACCESS_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
GOOGLE_SCOPE = 'openid email profile'

# DRF settings

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


# LIFETIME
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=500),  # Increase as needed
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1000),  # Increase as needed
}

# FrontEnd Settings
TOKEN_HANDLER_URL = "http://localhost:3000/token-handler"
# TOKEN_HANDLER_URL = "https://jobrobo.ai/token-handler"


# AWS settings
AWS_ACCESS_KEY_ID = "AKIATA7KDL3JSJTMXNVS"
AWS_SECRET_ACCESS_KEY = "rykvC6WEFe4FuYIMjeAm5bZMqS3DzdMnfjENyIRw"
AWS_STORAGE_BUCKET_NAME = 'jobrobo-django-bucket'
AWS_S3_REGION_NAME = 'us-east-2'  # e.g., us-east-1
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'


STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# OPEN API settings
# OPEN_AI_KEY = "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"
OPEN_AI_KEY = "sk-proj-scxdOOvocOVf7sEpEaAgT3BlbkFJhsdzEAHQIih77q8lTDLp"
OPEN_AI_MODEL = 'gpt-4o'

os.environ["OPENAI_API_KEY"] = "sk-proj-scxdOOvocOVf7sEpEaAgT3BlbkFJhsdzEAHQIih77q8lTDLp"

# Job scheduling settings
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IMPORTS = ('resumes.tasks', )


# CORS (for development only)
CORS_ALLOW_ALL_ORIGINS = True

# For production, something like this
# CORS_ALLOWED_ORIGINS = [
#        "http://:3000",
#    ]

CORS_ALLOW_CREDENTIALS = True


# For VectorDB and Langchains
TEMP_DIR = BASE_DIR / 'temp'
os.makedirs(TEMP_DIR, exist_ok=True)

DATASET_DIR = TEMP_DIR/'dataset'
os.makedirs(DATASET_DIR, exist_ok=True)

CHROMA_DIR = TEMP_DIR/'chroma_storage'
os.makedirs(CHROMA_DIR, exist_ok=True)
