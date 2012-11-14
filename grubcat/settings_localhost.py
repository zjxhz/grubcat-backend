# Django settings for grubcat project.

from settings import *

ASSETS_AUTO_BUILD = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'fanju', # Or path to database file if using sqlite3.
        'USER': 'fanju',
        'PASSWORD': 'fanju',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {"init_command": "SET storage_engine=INNODB", }
    }
}


