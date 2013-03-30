# Django settings for grubcat project.
import os
from django.core.urlresolvers import reverse_lazy

DEBUG = False
TEMPLATE_DEBUG = True

ADMINS = (
    ('Peter', 'ddsfeifei@gmail.com'),
    )


MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'fanju', # Or path to database file if using sqlite3.
        'USER': 'fanju',
        'PASSWORD': 'fan321',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {"init_command": "SET storage_engine=INNODB", }
    }
}

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'
DATE_FORMAT = 'Y n j'
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/fanju/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/home/fanju/webapps/static/'
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.CachedStaticFilesStorage"

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
#STATIC_URL = '/static/'
STATIC_URL = 'http://fanju.dn.qbox.me/'
# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
#ADMIN_MEDIA_PREFIX = '/static/admin/'

WEIBO_APP_KEY="4071331500"
WEIBO_APP_SECERT="5cf4910b217617cee72b2889a8e394eb"
WEIBO_REDIRECT_URL="http://www.fanjoin.com/login/weibo/"
# Make this unique, and don't share it with anybody.
SECRET_KEY = 'v**lqc)i)eeoiv#7=t6r&u-70auneuj#67yz*$%nez3p=)+8_d'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_assets.finders.AssetsFinder'
    # other finders..
    )

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'eo.exceptions.ProcessExceptionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware', # disable for mobile users temporarily
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    #    'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', 'eo.middlewares.WeiboAuthenticationBackend')
ROOT_URLCONF = 'grubcat.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\', '/'),
    #    'path/to/debug_toolbar/templates',
    )

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'eo',
    'django.contrib.staticfiles',
    'easy_thumbnails',
    'image_cropping',
    'tastypie',
    'django_assets',
    'south',
    'django_forms_bootstrap',
#    'ajax_select',
    'taggit',
    'raven.contrib.django',
    #    'debug_toolbar'
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    )

SERIALIZATION_MODULES = {
    'json': 'wadofstuff.django.serializers.json'
}

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "eo.util.chat_context_processor"
    )

#from easy_thumbnails.conf import settings as thumbnail_settings

#THUMBNAIL_PROCESSORS = (
#                           'image_cropping.thumbnail_processors.crop_corners',
#                           ) + thumbnail_settings.THUMBNAIL_PROCESSORS
#THUMBNAIL_QUALITY=100
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'easy_thumbnails.processors.scale_and_crop',
    'easy_thumbnails.processors.filters',)
BIG_AVATAR_SIZE = (220, 220)
NORMAL_AVATAR_SIZE = (80, 80)
SMALL_AVATAR_SIZE = (50, 50)
MEDIUM_AVATAR_SIZE = (150,150)
IMAGE_CROPPING_THUMB_SIZE = (360, 360)
THUMBNAIL_QUALITY = 100

AUTH_PROFILE_MODULE = 'eo.UserProfile'

#don't auto compress css/jss files, use command by manual
ASSETS_AUTO_BUILD = False
ASSETS_ROOT = r'/home/fanju/src/grubcat-backend/grubcat/eo/static'

#pay config
#30minutes
PAY_OVERTIME = 30

CHATSERVER = "http://www.fanjoin.com/http-bind/"
CHATDOMAIN = "fanjoin.com"












RAVEN_CONFIG = {
    'register_signals': True,
    'dsn': 'http://e113732a1ddc462f9183b1038e4af184:58a864b1292a40179f900fffc8d02b9e@www.fanjoin.com:9000/2',
    }

LOGGING_ROOT = "/home/fanju/logs/user/"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_ROOT, 'all.log'),
            'maxBytes': 1024 * 1024 * 2, # 5 MB
            'backupCount': 7,
            'formatter': 'verbose',
        },
        'pay': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_ROOT, 'pay.log'),
            'maxBytes': 1024 * 1024 * 2, # 5 MB
            'backupCount': 7,
            'formatter': 'verbose',
            },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['default'],
            'propagate': False,
        },
        'raven': {
            'level': 'ERROR',
            'handlers': ['default'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['default'],
            'propagate': False,
        },
        'api': {
            'handlers': ['default', 'sentry'],
            'level': 'DEBUG',
            'propagate': False
        },
        'pay': {
            'handlers': ['pay', 'sentry'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST =''
#EMAIL_PORT = 465
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD=''

#account
LOGIN_URL = reverse_lazy('weibo_login')
LOGIN_REDIRECT_URL = reverse_lazy('index')
RESTAURANT_LOGIN_URL = reverse_lazy('login')

SHOW_EXCEPTION_DETAIL = False

APP_ID = 'grubcat' # MAKE SURE THIS DOESN'T CONTAIN ANY PERIODS!
APNS_HOST = 'http://localhost:7077/'
APNS_CERTIFICATE_LOCATION = "/home/fanju/src/grubcat-backend/apns-dev.pem" # Created in step 2

XMPP_SERVER='localhost'
XMPP_PUBSUB_USER="pubsub" #'pubsub@fanjoin.com'
XMPP_PUBSUB_PASSWORD="fan321" #password for pubsub
XMPP_PUBSUB_SERVICE='pubsub.fanjoin.com'
XMPP_DEBUG=[]

try:
    from settings_dev import *
except Exception: pass

