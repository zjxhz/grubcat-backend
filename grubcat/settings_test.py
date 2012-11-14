# Django settings for grubcat project.
from settings import *
import os

TASTYPIE_FULL_DEBUG=True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'easyorder',                      # Or path to database file if using sqlite3.
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '',
        'TEST_CHARSET': 'UTF8'
    }
}

