from settings import *

#for test server

DEBUG = False
TEMPLATE_DEBUG = False
STATIC_URL = '/static/'
ASSETS_DEBUG = False
ASSETS_AUTO_BUILD = False

CHATSERVER = "http://www.ifunjoin.com/http-bind/"
CHATDOMAIN = "ifunjoin.com"
XMPP_PUBSUB_SERVICE = 'pubsub.ifunjoin.com'
ALIPAY_BACK_DOMAIN = 'http://www.ifunjoin.com/'
ORDER_PREFIX = 'det'
PAY_DEBUG = True

RAVEN_CONFIG = {
    'register_signals': False,
    # 'dsn': 'http://e113732a1ddc462f9183b1038e4af184:58a864b1292a40179f900fffc8d02b9e@www.fanjoin.com:9000/2',
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
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
            'level': 'INFO',
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
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

