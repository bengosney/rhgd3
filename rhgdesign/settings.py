# Standard Library
import os

# Third Party
import dj_database_url
from easy_thumbnails.conf import Settings as thumbnail_settings

##### START: botch for django-polymorphic
from django.core.exceptions import FieldDoesNotExist  # noqa: E402
from django.db import models  # noqa: E402
models.FieldDoesNotExist = FieldDoesNotExist
##### END: botch for django-polymorphic

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3zxyc$5xs3q7kj)m*1$8#b#w9mice9%)i#ci2$xt6+wczvu^5*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if os.environ.get('ENV') == 'production' else True

ALLOWED_HOSTS = ['*']

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'uploads')
CKEDITOR_URL = MEDIA_URL
CKEDITOR_JQUERY_URL = ('//ajax.googleapis.com/'
                       'ajax/libs/jquery/2.1.1/jquery.min.js')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'django.contrib.redirects',
    'django.contrib.sitemaps',
    'storages',
    'django_extensions',
    'image_cropping',
    'easy_thumbnails',
    'ckeditor',
    'ckeditor_uploader',
    'polymorphic_tree',
    'polymorphic',
    'mptt',
    'adminsortable2',
    'sorl.thumbnail',
    #'fontawesome',
    'modulestatus',
    'pages',
    'gardens',
    'websettings',
]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
    'rhgdesign.middleware.ProperURLMiddleware',
    'rhgdesign.middleware.ClacksOverhead',
]

ROOT_URLCONF = 'rhgdesign.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'pages.context_processors.nav_items',
                'gardens.context_processors.items',
                # 'django.core.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'rhgdesign.wsgi.application'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'rhgd'
AWS_QUERYSTRING_AUTH = False

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = 'apikey'
    EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY')


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DB_NAME = 'rhgdesign'
DB_USER = DB_NAME
DB_PASS = 'cJYuVv3uaBeP78Le'
DB_HOST = 'localhost'

if 'CIRCLECI' in os.environ:
    DB_NAME = 'circle_test'
    DB_USER = 'circleci'
    DB_PASS = ''
    DB_HOST = '127.0.0.1'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': DB_HOST,

    }
}

if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)


THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS

SITE_ID = 2

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

FONTAWESOME_CSS_URL = 'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css'

ROLLBAR = {
    'access_token': os.environ.get('ROLLBAR_TOKEN'),
    'environment': 'development' if DEBUG else 'production',
    'branch': 'master',
    'root': BASE_DIR,
}
