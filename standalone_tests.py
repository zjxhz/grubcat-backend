from django.http import HttpRequest
import os, sys
from grubcat.eo.views import *
from grubcat.eo.db import *

cwd = os.getcwd()
sys.stdout = sys.stderr
sys.path.append(cwd+'/grubcat/eo')
sys.path.append(cwd+'/grubcat')
sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'grubcat.settings'
print "hello django"
print hello(HttpRequest())
print updateLatLng(HttpRequest())
