
import os.path

CONF_ROOT = os.path.dirname(__file__)

DATABASES = {
'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'sentry', # Or path to database file if using sqlite3.
        'USER': 'tools',
        'PASSWORD': 'toolsfan321',
        'HOST': '',
        'PORT': '',
    }
}


SENTRY_KEY = 'JUSmmCnLwlPlgLMUnIojrGP+vlqWF6IEdjp4gbC6VEHz5O0702K2bg=='

# Set this to false to require authentication
SENTRY_PUBLIC = False

# You should configure the absolute URI to Sentry. It will attempt to guess it if you don't
# but proxies may interfere with this.
SENTRY_URL_PREFIX = 'http://42.121.34.164:9000'

SENTRY_WEB_HOST = '42.121.34.164'
SENTRY_WEB_PORT = 9000
SENTRY_WEB_OPTIONS = {
    'workers': 3,  # the number of gunicorn workers
    # 'worker_class': 'gevent',
}

# Mail server configuration

# For more information check Django's documentation:
#  https://docs.djangoproject.com/en/1.3/topics/email/?from=olddocs#e-mail-backends

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_HOST_PASSWORD = 'ddsjiayou124126'
#EMAIL_HOST_USER = 'ddsfeifei@gmail.com'
#EMAIL_PORT = 465
##EMAIL_USE_TLS = False

# http://twitter.com/apps/new
# It's important that input a callback URL, even if its useless. We have no idea why, consult Twitter.
TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''

# http://developers.facebook.com/setup/
FACEBOOK_APP_ID = ''
FACEBOOK_API_SECRET = ''

# http://code.google.com/apis/accounts/docs/OAuth2.html#Registering
GOOGLE_OAUTH2_CLIENT_ID = ''
GOOGLE_OAUTH2_CLIENT_SECRET = ''

# https://github.com/settings/applications/new
GITHUB_APP_ID = ''
GITHUB_API_SECRET = ''

# https://trello.com/1/appKey/generate
TRELLO_API_KEY = ''
TRELLO_API_SECRET = ''
