from settings import *

DEBUG = True
TEMPLATE_DEBUG = True
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# SESSION_COOKIE_DOMAIN = 'ifunjoin.com'
# SITE_DOMAIN = "http://192.168.1.2"
SITE_DOMAIN = "http://192.168.1.2"

SITE_ROOT = '/home/dds/site/'
LOGGING_ROOT = SITE_ROOT + "logs/"
STATIC_ROOT = SITE_ROOT + 'static/'
MEDIA_ROOT = SITE_ROOT + 'media/'
ASSETS_ROOT = SITE_ROOT + 'src/grubcat-backend/grubcat/fanju/static/'
GEOIP_PATH = SITE_ROOT + 'soft/'
# ASSETS_ROOT = STATIC_ROOT
ASSETS_AUTO_BUILD = True
ASSETS_DEBUG = True
def show_toolbar(request):
    return False
SHOW_TOOLBAR_CALLBACK = show_toolbar
INSTALLED_APPS += ('django_jenkins', 'debug_toolbar','cache_panel')
PROJECT_APPS = ('fanju', )

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'cache_panel.panel.CacheDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
MIDDLEWARE_CLASSES += (
    'devserver.middleware.DevServerMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
)
INTERNAL_IPS = ('127.0.0.1','192.168.1.2','t.ifunjoin.com:8001')
WEIBO_REDIRECT_URL = "http://127.0.0.1:8001/login/weibo/"
ALIPAY_BACK_DOMAIN = r'http://t.ifunjoin.com:8001/'
ORDER_PREFIX = 'ded1'
PAY_DEBUG = True

# CHATSERVER = "http://www.ifunjoin.com:8001/http-bind/"
CHATSERVER = "http://192.168.1.2/http-bind/"
CHATDOMAIN = "dds-ubuntu"
# XMPP_SERVER = 'dds-ubuntu'
XMPP_PUBSUB_SERVICE = 'pubsub.dds-ubuntu'


DEVSERVER_MODULES = (
    'devserver.modules.sql.SQLRealTimeModule',
    'devserver.modules.sql.SQLSummaryModule',
    'devserver.modules.profile.ProfileSummaryModule',

    # Modules not enabled by default
    'devserver.modules.ajax.AjaxDumpModule',
    'devserver.modules.profile.MemoryUseModule',
    # 'devserver.modules.cache.CacheSummaryModule',
    'devserver.modules.profile.LineProfilerModule',
)
INTERCEPT_REDIRECTS=True
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
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'level': 'WARNING',
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'INFO',
            'propagate': True,
        },
        'fanju': {
            'level': 'DEBUG',
            'propagate': True
        },
    }
}