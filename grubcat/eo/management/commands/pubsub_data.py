'''
Created on Mar 9, 2013

@author: wayne
'''
from django.core.management.base import BaseCommand
from grubcat.eo.models import UserProfile, Relationship, \
    pubsub_userprofile_created, user_followed, Meal, meal_created, MealParticipants, \
    meal_joined
import logging
logger = logging.getLogger('api')

class Command(BaseCommand):    
    def handle(self, *args, **options):
        logger.debug("Handle pubsub data")
        if args and args[0] == "--dry-run":
            self.dry_run = True
        else:
            self.dry_run = False
        self.signal_profile_created()
        self.signal_profile_followed()
        self.signal_meal_created()
        self.signal_meal_joined()
            
    def signal_profile_created(self):
        for profile in UserProfile.objects.all():
            if profile.weibo_id:
                if self.dry_run:
                    print u"creating nodes for user %s" % profile.user.username
                else:
                    pubsub_userprofile_created(self, profile, True)
    
    def signal_profile_followed(self):
        for relationship in Relationship.objects.all():
            followee = relationship.to_person
            if followee.weibo_id:
                if self.dry_run:
                    print u"creating nodes for following user %s" % followee.user.username
                else:
                    user_followed(self, relationship, True)
                    
    def signal_meal_created(self):
        for meal in Meal.objects.all():
            if self.dry_run:
                print u"creating nodes for meal %s, and the host %s is subscribing " % (meal, meal.host)
            else:
                meal_created(self, meal, True)
                
    def signal_meal_joined(self):
        for meal_participant in MealParticipants.objects.all():
            if meal_participant.userprofile.weibo_id:
                if self.dry_run:
                    print u"participant %s is subscribing meal %s" % (meal_participant.userprofile, meal_participant.meal)
                else:
                    meal_joined(self, meal_participant, True)
        
