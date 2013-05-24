'''
Created on Mar 9, 2013

@author: wayne
'''
from django.core.management.base import BaseCommand
import time
from fanju.models import User, Relationship, pubsub_user_created, user_followed, \
    Meal, meal_created, MealParticipants, meal_joined
from fanju.util import pubsub
from optparse import make_option
import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):    
    option_list = BaseCommand.option_list + ( make_option('--dry-run', action="store_true", dest="dry_run", default=False),
                                              make_option('--unsubscribe_owner_meal', action="store_true", dest="unsubscribe_own", default=False),)
    
    def handle(self, *args, **options):
        logger.debug("Handle pubsub data")
        self.dry_run = options.get("dry_run")
        if options.get("unsubscribe_own"):
            self.unsubscribe_owner_meal()
        self.signal_profile_created()
        time.sleep(5)
        self.signal_profile_followed()
        self.signal_meal_created()
        self.signal_meal_joined()
            
    def signal_profile_created(self):
        for profile in User.objects.all():
            # if profile.weibo_id:
            if self.dry_run:
                print u"creating nodes for user %s" % profile.id
            else:
                pubsub_user_created(self, profile, True)
    
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
                print u"creating nodes for meal %s" % (meal.id)
            else:
                meal_created(self, meal, True)
                
    def signal_meal_joined(self):
        for meal_participant in MealParticipants.objects.all():
            if self.dry_run:
                print u"participant %s is subscribing meal %s" % (
                    meal_participant.user.id, meal_participant.meal.id)
            else:
                meal_joined(self, meal_participant, True)

    def unsubscribe_owner_meal(self):
        for profile in User.objects.all():
            if profile.weibo_id:
                if self.dry_run:
                    print u"unsubscribing meal node for owner user %s" % profile.id
                else:
                    node_name = "/user/%d/meals" % profile.id
                    pubsub.unsubscribe(profile, node_name)
        
