'''
Created on Mar 9, 2013

@author: wayne
'''
from django.core.management.base import BaseCommand
import time
from fanju.models import User, Relationship, pubsub_user_created, user_followed, \
    Meal, meal_created, MealParticipants, meal_joined, OrderStatus, Order, _meal_joined
from fanju.util import pubsub
from optparse import make_option
import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):    
    option_list = BaseCommand.option_list + ( make_option('--dry-run', action="store_true", dest="dry_run", default=False),
                                              make_option('--unsubscribe_owner_meal', action="store_true", dest="unsubscribe_own", default=False),
                                              make_option('--action',  dest="action", default=False), )
    """
    if you want to delete old data first, use following sqls
    use openfire;
    delete FROM ofPubsubAffiliation;
    delete FROM ofPubsubNode;
    delete FROM ofPubsubSubscription;
    """
    def handle(self, *args, **options):
        logger.debug("Handle pubsub data")
        self.dry_run = options.get("dry_run")
        if options.get("unsubscribe_own"):
            self.unsubscribe_owner_meal()
            
        action = options.get("action")
        if not action:
            print "action required, specify any value of 'user_created | uc', 'user_followed | uf', 'meal_created | mc', 'meal_joined | mj', or 'all'"
            return
        
        if action == "all" or action == "user_created" or action == 'uc':
            self.user_created()
        time.sleep(5)
        if action == "all" or action == "user_followed" or action == 'uf':
            self.user_followed()
        if action == "all" or action == "meal_created" or action == 'mc':
            self.meal_created()
        if action == "all" or action == "meal_joined" or action == 'mj':
            self.meal_joined()
            
    def user_created(self):
        for profile in User.objects.all():
            # if profile.weibo_id:
            if self.dry_run:
                print u"creating nodes for user %s" % profile.id
            else:
                pubsub_user_created(self, profile, True)
    
    def user_followed(self):
        for relationship in Relationship.objects.all():
            followee = relationship.to_person
            follower = relationship.from_person
            # if followee.weibo_id and follower.weibo_id:
            if self.dry_run:
                print u"creating nodes for following user %s from user %s" % (
                    followee.id, relationship.from_person.id)
            else:
                user_followed(self, relationship, True)
                    
    def meal_created(self):
        for meal in Meal.objects.all():
            if self.dry_run:
                print u"creating nodes for meal %s" % (meal.id)
            else:
                meal_created(self, meal, True)
                
    def meal_joined(self):
        for order in Order.objects.filter(status__in=(OrderStatus.PAYIED, OrderStatus.USED)):
            if self.dry_run:
                print u"participant %s is subscribing meal %s" % (
                    order.customer.id, order.meal.id)
            else:
                _meal_joined(order.meal, order.customer)


    def unsubscribe_owner_meal(self):
        for profile in User.objects.all():
            if profile.weibo_id:
                if self.dry_run:
                    print u"unsubscribing meal node for owner user %s" % profile.id
                else:
                    node_name = "/user/%d/meals" % profile.id
                    pubsub.unsubscribe(profile, node_name)
        
