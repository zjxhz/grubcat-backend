'''
Created on Mar 9, 2013

@author: wayne
'''
from django.core.management.base import BaseCommand
from eo.util import pubsub
from eo.models import UserProfile, Relationship, \
    pubsub_userprofile_created, user_followed, Meal, meal_created, MealParticipants, \
    meal_joined
import logging
logger = logging.getLogger('api')

class Command(BaseCommand):    
    def handle(self, *args, **options):
        logger.debug("Handle pubsub data")
        if args and args[0] == "dry-run":
            self.dry_run = True
        elif args and args[0] == "unsubscribe-owner-meal":
            self.dry_run = False
            self.unsubscribe_owner_meal()
        else:
            self.dry_run = False
        self.signal_profile_created()
        self.signal_profile_followed()
        self.signal_meal_created()
        self.signal_meal_joined()
            
    def signal_profile_created(self):
        for profile in UserProfile.objects.all():
            # if profile.weibo_id:
            if self.dry_run:
                print u"creating nodes for user %s" % profile.id
            else:
                pubsub_userprofile_created(self, profile, True)
    
    def signal_profile_followed(self):
        for relationship in Relationship.objects.all():
            followee = relationship.to_person
            follower = relationship.from_person
            # if followee.weibo_id and follower.weibo_id:
            if self.dry_run:
                print u"creating nodes for following user %s from user %s" % (
                    followee.id, relationship.from_person.id)
            else:
                user_followed(self, relationship, True)
                    
    def signal_meal_created(self):
        for meal in Meal.objects.all():
            if self.dry_run:
                print u"creating nodes for meal %s, and host %s is subscribing " % (meal.id, meal.host.id)
            else:
                meal_created(self, meal, True)
                
    def signal_meal_joined(self):
        for meal_participant in MealParticipants.objects.all():
            # if meal_participant.userprofile.weibo_id:
            if self.dry_run:
                print u"participant %s is subscribing meal %s" % (
                    meal_participant.userprofile.id, meal_participant.meal.id)
            else:
                meal_joined(self, meal_participant, True)

    def unsubscribe_owner_meal(self):
        for profile in UserProfile.objects.all():
            if profile.weibo_id:
                if self.dry_run:
                    print u"unsubscribing meal node for owner user %s" % profile.id
                else:
                    node_name = "/user/%d/meals" % profile.id
                    pubsub.unsubscribe(profile, node_name)
        
