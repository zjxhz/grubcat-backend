import os
import sys

#sys.path = ['/home/fanju/webapps/django','/home/fanju/webapps/django/grubcat-backend','/home/fanju/webapps/django/grubcat-backend/grubcat', '/home/fanju/webapps/django/lib/python2.7'] + sys.path
#print sys.path
from django.core.handlers.wsgi import WSGIHandler

os.environ['DJANGO_SETTINGS_MODULE'] = 'grubcat.settings'
application = WSGIHandler()
