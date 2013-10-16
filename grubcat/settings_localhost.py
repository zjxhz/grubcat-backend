# Django settings for grubcat project.

from settings import *
ASSETS_DEBUG=True
ASSETS_AUTO_BUILD = True
STATIC_URL = '/static/'
DEBUG=True
XMPP_SERVER="localhost"
ORDER_PREFIX = 'dew'

RAVEN_CONFIG = {
    'register_signals': False,
    # 'dsn': 'http://e113732a1ddc462f9183b1038e4af184:58a864b1292a40179f900fffc8d02b9e@www.fanjoin.com:9000/2',
    }

LOGGING_ROOT = "/Users/wayne/temp/"


#INSTALLED_APPS += ('debug_toolbar','devserver')
MEDIA_ROOT = '/Users/wayne/workspace/media/'
ASSETS_ROOT = r'/Users/wayne/workspace/grubcat-backend/grubcat/fanju/static'
LESS_BIN="/usr/local/bin/lessc"
ASSETS_AUTO_BUILD = True
XMPP_DEBUG = []
PAY_DEBUG = True
TASTYPIE_FULL_DEBUG = True
CHATSERVER = "http://localhost:7070/http-bind/"
CHATDOMAIN = "wayne.local"
XMPP_PUBSUB_SERVICE='pubsub.wayne.local'

RAVEN_CONFIG = {
    'register_signals': False,
    # 'dsn': 'http://e113732a1ddc462f9183b1038e4af184:58a864b1292a40179f900fffc8d02b9e@www.fanjoin.com:9000/2',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
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
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'INFO',
            'propagate': True,
        },
        'fanju': {
            'level': 'DEBUG',
            'propagate': True
        },
        'gunicorn.error': {
            'level': 'ERROR',
            'handlers': ['gunicorn_error'],
            'propagate': True,
        },
    }
}

GEOIP_PATH = '/Users/wayne/workspace/fanju_resources/geo'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}