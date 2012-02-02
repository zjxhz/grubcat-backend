# this file is for dotcloud
import os, sys
cwd = os.getcwd()
sys.stdout = sys.stderr
sys.path.append(cwd+'/grubcat/eo')
sys.path.append(cwd+'/grubcat')
sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'grubcat.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
