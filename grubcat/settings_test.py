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

WEIBO_APP_KEY = "1086545555"
WEIBO_APP_SECERT = "edc858db52e5c2bc803010a81b183c5d"
WEIBO_REDIRECT_URL = "http://www.ifunjoin.com/login/weibo/"

RAVEN_CONFIG = {
    'register_signals': True,
    'dsn': 'http://66a385f77d6a4fa3ab75db245d66695a:0d7f487d06a74dbaa634d894f77703d6@www.ifunjoin.com:9000/2',
    }


