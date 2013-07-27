import os
from django.core.urlresolvers import reverse_lazy

#for product server

###
FREE_PAY_USER_ID = ('1652340607', '', '')

###################### app ######################
DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ('*.fanjoin.com', 'localhost', '127.0.0.1', '*.ifunjoin.com', '*.ifunjoin.com:8001')
SITE_ROOT = '/home/fanju/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'fanju', # Or path to database file if using sqlite3.
        'USER': 'fanju',
        'PASSWORD': 'fan321',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {"init_command": "SET storage_engine=INNODB", }
    },
    'openfire': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'openfire', # Or path to database file if using sqlite3.
        'USER': 'fanju',
        'PASSWORD': 'fan321',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {"init_command": "SET storage_engine=INNODB", }
    }
}

ADMINS = (
    ('Peter', 'ddsfeifei@gmail.com'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'v**lqc)i)eeoiv#7=t6r&u-70auneuj#67yz*$%nez3p=)+8_d'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'fanju.exceptions.ProcessExceptionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware', # disable for mobile users temporarily
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    )

ROOT_URLCONF = 'grubcat.urls'

INSTALLED_APPS = (

    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'fanju',
    'django.contrib.staticfiles',
    'easy_thumbnails',
    'image_cropping',
    'tastypie',
    'django_assets',
    'south',
    'django_forms_bootstrap',
    'taggit',
    'raven.contrib.django.raven_compat',
    'admin_user_stats',
    'chart_tools',
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    #  'grappelli.dashboard',
    # 'grappelli',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.admin',
    'djcelery',
    'kombu.transport.django',
    'clear_cache',
    'cacheops',
    'django_pickling'

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
    "fanju.util.common_context_processor"
)

MANAGERS = ADMINS
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
SITE_DOMAIN = "http://fanjoin.com"

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

AUTH_USER_MODEL = 'fanju.User'


##################### chache ######################

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        # 'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': '127.0.0.1:6379',
        'TIMEOUT': 3600,
        # 'JOHNNY_CACHE' : True,
        'OPTIONS': {
            # 'DB': 1,
            # 'PASSWORD': 'yadayada',
            'MAX_ENTRIES': 50000,
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        },
        'KEY_PREFIX': 'fj'
    },
}
CACHE_MIDDLEWARE_SECONDS = 3600
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7

CACHEOPS_REDIS = {
    'host': 'localhost', # redis-server is on same machine
    'port': 6379,        # default redis port
    'db': 1,             # SELECT non-default redis database
                         # using separate redis db or redis instance
                         # is highly recommended
    'socket_timeout': 3,
}

CACHEOPS = {
    # Automatically cache any User.objects.get() calls for 15 minutes
    # This includes request.user or post.author access,
    # where Post.author is a foreign key to auth.User
    'fanju.meal': ('all', 60 * 60 * 6),
    'fanju.restaurant': ('all', 60 * 60 * 12),
    'fanju.userlocation': ('all', 60 * 60 * 12),
    'fanju.menu': ('all', 60 * 60 * 12),
    'fanju.dish': ('all', 60 * 60 * 12),
    'fanju.dishcategory': ('all', 60 * 60 * 12),
    'fanju.userphoto': ('all', 60 * 10),
    'fanju.visitor': ('all', 60 * 10),
    'fanju.relationship': ('all', 60 * 10),
    'fanju.mealcomment': ('all', 60 * 60),
    'fanju.usercomment': ('all', 60 * 60),
    'fanju.photocomment': ('all', 60 * 60),
    'fanju.meallike': ('all', 60 * 60),
    'fanju.photolike': ('all', 60 * 60),
    'fanju.user': ('get', 60 * 60 * 1),
    'fanju.order': ('get', 60 * 60),
    # 'fanju.usertag': ('all', 60 * 60),
    # 'fanju.taggeduser': ('all', 60 * 60),
    # 'taggit_tag': ('all', 60 * 60),

    # Automatically cache all gets, queryset fetches and counts
    # to other django.contrib.auth models for an hour
    # 'auth.*': ('all', 60*60),

    # Enable manual caching on all news models with default timeout of an hour
    # Use News.objects.cache().get(...)
    #  or Tags.objects.filter(...).order_by(...).cache()
    # to cache particular ORM request.
    # Invalidation is still automatic
    # 'news.*': ('just_enable', 60*60),

    # Automatically cache count requests for all other models for 15 min
    # '*.*': ('count', 60*15),
}
CACHEOPS_DEGRADE_ON_FAILURE=True
###################### static ######################
STATIC_URL = '/static/'
# STATIC_URL = 'http://fanju.dn.qbox.me/'
STATIC_ROOT = SITE_ROOT + 'static/'
ASSETS_DEBUG = False
ASSETS_AUTO_BUILD = False
ASSETS_ROOT = SITE_ROOT + 'src/grubcat-backend/grubcat/fanju/static'
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.CachedStaticFilesStorage"
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django_assets.finders.AssetsFinder'
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\', '/'),
    #    'path/to/debug_toolbar/templates',
)

###################### media ######################
MEDIA_URL = '/media/'
MEDIA_ROOT = SITE_ROOT + 'media/'
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'easy_thumbnails.processors.scale_and_crop',
    'easy_thumbnails.processors.filters',)
VALID_IMAGE_FORMATS = ('image/png', 'image/jpg', 'image/jpeg', 'image/pjpeg')
AVATAR_MIN_WIDTH = 180
AVATAR_MIN_HEIGHT = 180
AVATAR_MAX_SIZE = 4 #MB
PHOTO_MIN_WIDTH = 180
PHOTO_MIN_HEIGHT = 180
PHOTO_MAX_SIZE = 4048


THUMBNAIL_QUALITY = 90
BIG_AVATAR_SIZE = (180, 180)
MEDIUM_AVATAR_SIZE = (150, 150)
NORMAL_AVATAR_SIZE = (80, 80)
SMALL_AVATAR_SIZE = (50, 50)
IMAGE_CROPPING_THUMB_SIZE = (360, 360)
BIG_MENU_COVER_SIZE = (420, 280)
NORMAL_MENU_COVER_SIZE = (360, 240)
SMALL_MENU_COVER_SIZE = (150, 100)
MINI_MENU_COVER_SIZE = (60, 40)

#relative to media root
DEFAULT_MALE_AVATAR = 'default/male.png'
DEFAULT_FEMALE_AVATAR = 'default/female.png'


###################### pay ######################
PAY_OVERTIME = 35
PAY_OVERTIME_FOR_PAY_OR_USER = 30 # should smaller than PAY_OVERTIME, because alipay has a delay
PAY_DEBUG = False
ORDER_PREFIX = 'po3'
ALIPAY_BACK_DOMAIN = 'http://fanjoin.com/'

###################### email ######################
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST =''
#EMAIL_PORT = 465
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD=''

###################### acount ######################
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', 'fanju.middlewares.WeiboAuthenticationBackend')
LOGIN_URL = reverse_lazy('weibo_login')
LOGIN_REDIRECT_URL = reverse_lazy('index')
RESTAURANT_LOGIN_URL = reverse_lazy('login')

WEIBO_OFFICIAL = '3193907700'
WEIBO_APP_KEY = "2295468526"
WEIBO_APP_SECERT = "5991184a22eaff8d2b1149bcf1b1ff91"
WEIBO_REDIRECT_URL = "http://fanjoin.com/login/weibo/"

###################### apple push ######################
APP_ID = 'grubcat' # MAKE SURE THIS DOESN'T CONTAIN ANY PERIODS!
APNS_HOST = 'http://localhost:7077/'
APNS_CERTIFICATE_LOCATION = "/home/fanju/src/grubcat-backend/apns_combine.pem" # Created in step 2
APNS_ENVIRONMENT='production'


###################### xmpp chat ######################
XMPP_SERVER = 'localhost'
XMPP_PUBSUB_SERVICE = 'pubsub.fanjoin.com'
XMPP_DEBUG = []
CHATSERVER = "http://fanjoin.com/http-bind/"
CHATDOMAIN = "fanjoin.com"


###################  admin #######################
ADMIN_TOOLS_INDEX_DASHBOARD = 'grubcat.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'grubcat.dashboard.CustomAppIndexDashboard'

################### celery #######################
import djcelery
djcelery.setup_loader()

BROKER_URL = 'redis://localhost:6379/0'
# BROKER_URL = 'django://'

###################### msic ######################
SHOW_EXCEPTION_DETAIL = False
GEOIP_PATH = SITE_ROOT + 'soft/'
FAKED_LAT = 30.275
FAKED_LNG = 120.148
###################### log ######################
RAVEN_CONFIG = {
    'dsn': 'http://0110aabffb89455db2b86848b0694351:c2cd2b4d540e47baa418ebe1d4249fad@fanjoin.com:9000/2',
}

LOGGING_ROOT = SITE_ROOT + "logs/user/"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
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
        'api': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_ROOT, 'api.log'),
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
            'class': 'raven.handlers.logging.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'gunicorn_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 2, # 5 MB
            'backupCount': 7,
            'formatter': 'verbose',
            'filename': os.path.join(LOGGING_ROOT, 'gunicorn_error.log')
        },

    },
    'loggers': {
        '': {
            'handlers': ['default', 'sentry'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django': {
            'level': 'ERROR',
            'propagate': True
        },
        'fanju': {
            'level': 'DEBUG',
            'propagate': True
        },
        'fanju.apis': {
            'handlers': ['api'],
            'level': 'DEBUG',
            'propagate': True
        },
        'fanju.pay': {
            'handlers': ['pay', 'sentry'],
            'level': 'DEBUG',
            'propagate': False
        },

        'gunicorn.error': {
            'level': 'ERROR',
            'handlers': ['gunicorn_error'],
            'propagate': True,
        },
    }
}