# Django settings for grubcat project.

from settings import *

ASSETS_AUTO_BUILD = True
STATIC_URL = '/static/'
DEBUG=True
XMPP_SERVER="localhost"
LOGGING_ROOT = "/Users/wayne/temp/"

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
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'api': {
            'handlers': ['console', 'sentry'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

#INSTALLED_APPS += ('debug_toolbar','devserver')
MEDIA_ROOT = '/Users/wayne/workspace/media'
ASSETS_ROOT = r'/Users/wayne/workspace/grubcat-backend/grubcat/eo/static'
LESS_BIN="/usr/local/bin/lessc"
ASSETS_AUTO_BUILD = True
XMPP_DEBUG=["socket"]
#os.path.join("/usr/local/", "bin")