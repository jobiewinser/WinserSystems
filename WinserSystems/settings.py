"""
Django settings for WinserSystems project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os 
from dotenv import load_dotenv
from pathlib import Path  # python3 only
from corsheaders.defaults import default_headers

env_path = Path('/var/www/WinserSystems/.env')
load_dotenv(dotenv_path=env_path)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'level': 'DEBUG'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': "debug.log",
        }
        # 'active_campaign_webhook': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'formatter': 'file',
        #     'filename': "active_campaign_webhook.log",
        # },
        # 'whatsapp_webhook': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'formatter': 'file',
        #     'filename': "whatsapp_webhook.log",
        # },
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console', 'file']
        },
    }
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
if os.getenv('ENVIRONMENT') == 'development':
    ALLOWED_HOSTS = ['*']
    DEBUG = True
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "staticfiles"),
    )
    INTERNAL_IPS = ['127.0.0.1',]

else:
    ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS'), '*']
    DEBUG = False
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "staticfiles"),
    )

# if DEBUG:
WHATSAPP_PHONE_OVERRIDE1=None
WHATSAPP_PHONE_OVERRIDE2='447974214718'
WHATSAPP_PHONE_OVERRIDE3='447506372794'
ENABLE_WHATSAPP_MESSAGING = os.getenv('ENABLE_WHATSAPP_MESSAGING') == 'True'

# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'campaign_leads',
    'active_campaign',
    'whatsapp',
    'messaging',
    'twilio',
    'calendly',
    'analytics',
    'core',
    'import_export',
    # 'rest_framework',
    'channels',
    'hijack',
    'hijack.contrib.admin',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'hijack.middleware.HijackUserMiddleware',
]

ROOT_URLCONF = 'WinserSystems.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR,'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR,],
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

WSGI_APPLICATION = 'wsgi.application'
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

#DATABASES = {
#   'default': {
 #       'ENGINE': 'django.db.backends.sqlite3',
 #       'NAME': BASE_DIR / 'db.sqlite3',
 #   }
#}

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME':os.getenv("DBNAME"),
        'USER':os.getenv("DBUSER"),
        'PASSWORD':os.getenv("DBPASSWORD"),
        'HOST':'localhost',
        'PORT':'',
    }
}
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

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# auth_classes = [
#         "rest_framework.authentication.SessionAuthentication",
#         # "api.authentication.TokenAuthentication"               
# ]
    
# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": auth_classes,
    
#     "DEFAULT_PERMISSION_CLASSES": [
#         # "rest_framework.permissions.IsAuthenticatedOrReadOnly",
#         "rest_framework.permissions.AllowAny"
#     ],
#     "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
#     "PAGE_SIZE": 25,
#     'DEFAULT_RENDERER_CLASSES': (
#         'rest_framework.renderers.JSONRenderer', #DO NOT REMOVE, VIEWFLOW NEEDS THIS???
#         'rest_framework.renderers.TemplateHTMLRenderer', #DO NOT REMOVE, VIEWFLOW NEEDS THIS???
#     )
# }

CORS_ALLOWED_ORIGINS = [
    'https://app.winser.uk',
    # '82.37.38.164'
]
CSRF_TRUSTED_ORIGINS = ['https://app.winser.uk']

CORS_REPLACE_HTTPS_REFERER = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    "Access-Control-Allow-Origin",
]


LOGIN_REDIRECT_URL = "/campaign-leads/leads-and-calls/"
LOGOUT_REDIRECT_URL = "/"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

ASGI_APPLICATION = "WinserSystems.routing.application" #routing.py will be created later
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': "channels_redis.core.RedisChannelLayer"
        }
}


LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/customer-login/'
LOGOUT_REDIRECT_URL = '/customer-login/'

# django login as other https://django-hijack.readthedocs.io/en/stable/
# Where admins are redirected to after hijacking a user
HIJACK_LOGIN_REDIRECT_URL = '/customer-login/'
# Where admins are redirected to after releasing a user
HIJACK_LOGOUT_REDIRECT_URL = '/customer-login/'
HIJACK_USE_BOOTSTRAP = True
HIJACK_ALLOW_GET_REQUESTS = True
HIJACK_PERMISSION_CHECK = "core.hijack.permissions.superusers_hijack"