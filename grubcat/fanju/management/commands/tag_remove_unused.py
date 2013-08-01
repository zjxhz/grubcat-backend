'''
Created on Jun 8, 2013

@author: wayne
'''
from django.core.management.base import BaseCommand
from fanju.models import UserTag

class Command(BaseCommand):    
    def handle(self, *args, **options):
        for tag in UserTag.objects.all():
            if tag.tagged_users():
                continue
            else:
                print 'tag(id=%s) %s is not used by anyone' % (tag, tag.id)