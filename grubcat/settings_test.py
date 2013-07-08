from settings import *

#for test server

DEBUG = False
TEMPLATE_DEBUG = False
STATIC_URL = '/static/'
ASSETS_DEBUG = False
ASSETS_AUTO_BUILD = False

SITE_DOMAIN = "http://t.ifunjoin.com"
CHATSERVER = SITE_DOMAIN + "/http-bind/"
CHATDOMAIN = "ifunjoin.com"
XMPP_PUBSUB_SERVICE = 'pubsub.ifunjoin.com'
ALIPAY_BACK_DOMAIN = SITE_DOMAIN + "/"

ORDER_PREFIX = 'det1'
PAY_DEBUG = False
XMPP_DEBUG = ['socket']

#WEIBO_APP_KEY = "4071331500"
#WEIBO_APP_SECERT = "5cf4910b217617cee72b2889a8e394eb"

WEIBO_APP_KEY = "1086545555"
WEIBO_APP_SECERT = "edc858db52e5c2bc803010a81b183c5d"
WEIBO_REDIRECT_URL = SITE_DOMAIN + "login/weibo/"

RAVEN_CONFIG = {
    'register_signals': True,
    'dsn': 'http://66a385f77d6a4fa3ab75db245d66695a:0d7f487d06a74dbaa634d894f77703d6@ifunjoin.com:9000/2',
    }

APNS_CERTIFICATE_LOCATION = "/home/fanju/src/grubcat-backend/apns-dev_combine.pem" 
APNS_ENVIRONMENT='sandbox'
