"""
Django settings for ccm project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a@m_u@22l@r0m)pgkm(unp2dll-14ms&aw%e-svhrdf$g657us'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)s [%(threadName)s] [%(name)s] %(pathname)s %(funcName)s %(lineno)d: %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s [%(threadName)s] [%(name)s] %(message)s'
        },
    },
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
        # 'mail_admins': {
        #     'level': 'ERROR',
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     'include_html': True,
        #     'formatter': 'standard'
        # },
        # 'file_handler': {
        #      'level': 'DEBUG',
        #      'class': 'logging.handlers.TimedRotatingFileHandler',
        #      'filename': os.path.join(BASE_DIR, "server.log"),
        #      'when': 'D',
        #      'interval': 7,
        #      'backupCount': 2,
        #      'encoding': 'UTF-8',
        #      'formatter': 'standard'
        # },
        'server_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "server.log"),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'encoding': 'UTF-8',
            'formatter': 'standard'
        },
        'samples_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "samples.log"),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'encoding': 'UTF-8',
            'formatter': 'standard'
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['server_log', 'console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
            'propagate': False,
        },
        # 'django.request': {
        #     'handlers': ['mail_admins'],
        #     'level': os.getenv('DJANGO_REQUEST_LOG_LEVEL', 'ERROR'),
        #     'filters': ['require_debug_false'],
        #     'propagate': False,
        # },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'ccm': {
            'handlers': ['server_log', 'console'],
            'level': os.getenv('CCM_LOG_LEVEL', 'DEBUG'),
            'propagate': False
        },
        'samples': {
            'handlers': ['samples_log', 'console'],
            'level': os.getenv('RETRIEVE_LOG_LEVEL', 'DEBUG'),
            'propagate': False
        },
    }
}

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'django_crontab',
    'ccmapp'
]

# Before python manage.py, you may have to run python manage.py crontab add
CRONJOBS = [
    ('0 8 * * *', 'ccmapp.cron.update_samples_task'),
    ('0 9 * * *', 'ccmapp.cron.fetch_video_task')
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ccm.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'TEMPLATE_DIRS': [os.path.join( os.path.split( os.path.dirname(__file__))[0],'templates').replace('\\','/'),],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]


WSGI_APPLICATION = 'ccm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydb',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '123456'
    }
}


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


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    # ),
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework.authentication.SessionAuthentication',
    #     'rest_framework.authentication.BasicAuthentication'
    # ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        #  Enable BrowsableAPI
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend', 'rest_framework.filters.OrderingFilter'
    ),
    'DEFAULT_PAGINATION_CLASS': 'ccmapp.pagination.CustomizedPageNumberPagination',
    'PAGE_SIZE': 500
}


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

#USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
# AUTH_USER_MODEL = 'ccmapp.BuildingCompanyUser'


LOGIN_REDIRECT_URL='/index/'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #os.path.join( os.path.dirname(__file__),'templates').replace('\\','/'),
    os.path.join( os.path.split( os.path.dirname(__file__))[0],'templates').replace('\\','/'),
)

UPLOAD_BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_DIR=os.path.join(os.path.split(UPLOAD_BASE_DIR)[0], 'upload/' ).replace('\\','/')
DOCTEMPLATE_DIR=os.path.join(os.path.split(UPLOAD_BASE_DIR)[0], 'doctemplate/' ).replace('\\','/')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = (
    ("css",os.path.join(STATIC_ROOT, 'css')),
    ("js",os.path.join(STATIC_ROOT, 'js')),
    ("fonts",os.path.join(STATIC_ROOT, 'fonts')),
    ("img",os.path.join(STATIC_ROOT, 'img')),
    ("ico",os.path.join(STATIC_ROOT, 'ico')),
    ("textures",os.path.join(STATIC_ROOT, 'textures')),
)

STATIC_PATH = os.path.join( os.path.split( os.path.dirname(__file__))[0],'static/').replace('\\','/')

IS_LOCAL_DEBUG = True

X_FRAME_OPTIONS = 'ALLOWALL'
