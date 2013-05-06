import os
import sys
path = ['/home/fanju/src/grubcat-backend','/home/fanju/src/grubcat-backend/grubcat']
sys.path=path+sys.path

from django.core.handlers.wsgi import WSGIHandler

os.environ['DJANGO_SETTINGS_MODULE'] = 'grubcat.settings'
application = WSGIHandler()
