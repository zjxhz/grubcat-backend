'''
Created on Mar 9, 2013

@author: wayne
'''
from django.core.management.base import BaseCommand
import time
from fanju.models import User, Relationship, pubsub_user_created, user_followed, \
    Meal, MealParticipants, meal_joined, OrderStatus, Order, _meal_joined
import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):    

    def handle(self, *args, **options):
        logger.debug("check data")
        user_list = [uid[0] for uid in User.objects.all().values_list('id')]
        meal_list = [mid[0] for mid in Meal.objects.all().values_list('id')]

        for meal in Meal.objects.all():
            if meal.host_id and meal.host_id not in user_list:
                print ("host %s not exist, meal_id=%s" % (meal.host_id, meal.id))

        for relation in Relationship.objects.all():
            if relation.from_person_id not in user_list:
                print ("follower %s not exist, relation_id=%s" % (relation.from_person_id, relation.id))
            if relation.to_person_id not in user_list:
                print ("followee %s not exist, relation_id=%s" % (relation.to_person_id, relation.id))

        for participant in MealParticipants.objects.all():
            if participant.user_id not in user_list:
                print ('user %s not exist, participant_id=%s' % (participant.user_id, participant.id))

            if participant.meal_id not in meal_list:
                print ('meal %s not exist, participant_id=%s' % ( participant.meal_id, participant.id))

