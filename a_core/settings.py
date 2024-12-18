"""
Django settings for a_core project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import dj_database_url

# for environment
from environ import Env
env = Env()
Env.read_env()
ENVIRONMENT = env('ENVIRONMENT', default='production')
# ENVIRONMENT='production'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-r9yx76es#x^2%7%e(hjomn=lwriy4ir56zr*2cg31_p5^qu7qk'
SECRET_KEY = env('SECRET_KEY')

# ENCRYPT_KEY = b'kVHxD3E5GAIzFsLN0deB6umZFwiVWzE6GnUOFBA8-Xo='
ENCRYPT_KEY = env('ENCRYPT_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# for environment
if ENVIRONMENT == 'development':
    DEBUG = True
else:
    DEBUG = False

# site_domain = env('RAILWAY_PUNLIC_DOMAIN', default='')
# ALLOWED_HOSTS = ['localhost', '127.0.0.1', site_domain]
# CSRF_TRUSTED_ORIGINS = [ f'https://{site_domain}' ]

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'celeryflowerbeat.up.railway.app' ]
CSRF_TRUSTED_ORIGINS = [ 'https://celeryflowerbeat.up.railway.app' ]

INTERNAL_IPS = (
    '127.0.0.1',
    'localhost:8000'
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # for django_cleanup    
    'django_cleanup.apps.CleanupConfig',
    # for media server
    'cloudinary_storage', 
    'cloudinary',     
    # for allauth    
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    # for django_htmx
    'django_htmx',
    'a_home',
    'a_users',
    'a_messageboard',
    'django_celery_results',
    'django_celery_beat',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # for allauth  
    'allauth.account.middleware.AccountMiddleware',
    # for django_htmx
    'django_htmx.middleware.HtmxMiddleware',
    # for whitenoise
    "whitenoise.middleware.WhiteNoiseMiddleware",    
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ROOT_URLCONF = 'a_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
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

WSGI_APPLICATION = 'a_core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if ENVIRONMENT == 'development':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(env('DATABASE_URL'))
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

# USE_TZ = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [ BASE_DIR / 'static' ]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# for media server
MEDIA_URL = 'media/'
if ENVIRONMENT == "production":
    STORAGES = {
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
            },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
            },
    }
    CLOUDINARY_STORAGE = {
        # 'CLOUD_NAME': env('CLOUD_NAME'),
        # 'API_KEY': env('API_KEY'),
        # 'API_SECRET': env('API_SECRET'),
        'CLOUDINARY_URL':env('CLOUDINARY_URL')    
    }    
else:      
    MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
ACCOUNT_SIGNUP_REDIRECT_URL = "{% url 'account_signup' %}?next={% url 'profile-onboarding' %}"

# for email authentication
if ENVIRONMENT == "production" or ENVIRONMENT == "development":
# if ENVIRONMENT == "production":           
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = env('EMAIL_ADDRESS')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    # DEFAULT_FROM_EMAIL = 'Awesome'
    DEFAULT_FROM_EMAIL = f'Celery {env("EMAIL_ADDRESS")}'      # <===Awesome은 Django App Name(DeployDaphneRedis)
    ACCOUNT_EMAIL_SUBJECT_PREFIX = ''
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True

# CELERY SETTINGS
if ENVIRONMENT == "development":
    CELERY_BROKER_URL = 'redis://localhost:6379/0' 
else:
    CELERY_BROKER_URL = env('REDIS_URL')
    
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_EXTENDED = True
