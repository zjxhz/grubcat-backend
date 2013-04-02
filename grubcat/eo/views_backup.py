#coding=utf-8
# Create your views here.
from datetime import datetime
from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from eo.models import Restaurant, RestaurantInfo, Rating, Dish, Order,\
    BestRatingDish, RestaurantTag, Region, Relationship, UserMessage, Meal, MealInvitation
from grubcat.eo.forms import *
import sys
import json

from django.conf import settings
def writeJson(qs, response, relations=None):
    json_serializer = serializers.get_serializer("json")()
    if relations:
        return json_serializer.serialize(qs, ensure_ascii=False, relations=relations, stream=response)
    return json_serializer.serialize(qs, ensure_ascii=False, stream=response)


def getJsonResponse(qs, relations=None):
    response = HttpResponse(content_type='application/json')
    writeJson(qs, response, relations)
    return response

def createGeneralResponse(status, message, extra_dict=None):
    response = {'status': status, 'info': message}
    if extra_dict:
        response.update(extra_dict)
    return HttpResponse(json.dumps(response))

# get distance in meter, code from google maps
def getDistance( lng1, lat1, lng2, lat2):
    EARTH_RADIUS = 6378.137
    from math import asin, sin, cos, radians, pow, sqrt

    radLat1 = radians(lat1)
    radLat2 = radians(lat2)
    a = radLat1 - radLat2
    b = radians(lng1) - radians(lng2)
    s = 2 * asin(sqrt(pow(sin(a / 2), 2) + cos(radLat1) * cos(radLat2) * pow(sin(b / 2), 2)))
    s = s * EARTH_RADIUS
    return s * 1000

# convert the query set of models to a list of dict
def modelToDict(query_set, relations=None):
    serializer = serializers.get_serializer("json")()
    if relations:
        return json.loads(serializer.serialize(query_set, relations=relations))
    return json.loads(serializer.serialize(query_set))


def restaurantList(request):
    key = request.GET.get('key')
    if key:
        return getJsonResponse(Restaurant.objects.filter(name__contains=key))
    return getJsonResponse(Restaurant.objects.all())


def get_restaurant(request, restaurant_id):
    response = HttpResponse()
    r = Restaurant.objects.get(id=restaurant_id)
    jsonR = modelToDict([r])[0]
    try:
        ri = RestaurantInfo.objects.get(restaurant__id=restaurant_id)
        jsonR['fields']['rating'] = ri.average_rating
        jsonR['fields']['average_cost'] = ri.average_cost
        jsonR['fields']['good_rating_percentage'] = ri.good_rating_percentage
        jsonR['fields']['comments'] = modelToDict(Rating.objects.filter(restaurant__id=restaurant_id),
            {'user': {'fields': ('username',)}})
        jsonR['fields']['recommended_dishes'] = modelToDict(r.get_recommended_dishes(),
            {'user': {'fields': ('username',)}, 'dish': {'fields': ('name',)}})
    except ObjectDoesNotExist:
        jsonR['fields']['rating'] = -1
        jsonR['fields']['average_cost'] = -1
        jsonR['fields']['good_rating_percentage'] = -1
        jsonR['fields']['comments'] = []
        jsonR['fields']['recommended_dishes'] = []
    response.write(json.dumps(jsonR, ensure_ascii=False))
    return response


def get_recommended_dishes(request, restaurant_id):
    response = HttpResponse()
    dishes = Restaurant.objects.get(id=restaurant_id).get_recommended_dishes()
    writeJson(dishes, response, ('dish',)) # order by dish descending
    return response

# return a list of values with the order how keys are sorted for a given dict
def sortedDictValues(some_dict):
    keys = some_dict.keys()
    keys.sort()
    return [some_dict[key] for key in keys]


def get_restaurant_list_by_geo(request):
    try:
        response = HttpResponse()
        lng = float(request.GET.get('longitude'))
        lat = float(request.GET.get('latitude'))
        rangeInMeter = float(request.GET.get('range'))
        # TODO page...
        distance_restaurant_dict = {}
        rating_restaurant_dict = {}
        cost_restaurant_dict = {}
        order_by = request.GET.get('order_by')
        restaurants = []
        for r in Restaurant.objects.all():
            if r.longitude and r.latitude:
                distance = getDistance(lng, lat, r.longitude, r.latitude)
                if distance < rangeInMeter:
                    if order_by == 'distance':
                        distance_restaurant_dict[distance] = r
                    elif order_by == 'cost':
                        cost_restaurant_dict[r.average_cost] = r
                    elif order_by == 'rating':
                        print "%s rating: %s" % (r, r.rating)
                        rating_restaurant_dict[r.rating] = r
                    else:
                        restaurants.append(r)
        if order_by == 'distance':
            restaurants = sortedDictValues(distance_restaurant_dict)
        elif order_by == 'cost':
            restaurants = sortedDictValues(cost_restaurant_dict)
        elif order_by == 'rating':
            print "before reverse_lazy: %s" % sortedDictValues(rating_restaurant_dict)
            restaurants = sortedDictValues(rating_restaurant_dict)
            restaurants.reverse_lazy()
            # print "Restaruants in range %s meters: %s" % (rangeInMeter, distance_restaurant_dict)
        writeJson(restaurants, response)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    return  response


def login_required_response(request):
    response = {"status": "NOK", "info": "You were not logged in"}
    return HttpResponse(json.dumps(response))


def order_last_modified(request, order_id):
    return Order.objects.get(id=order_id).confirmed_time


def get_orders(request):
    if not request.user.is_authenticated():
        return login_required_response(request)
    response = HttpResponse()
    serializer = serializers.get_serializer("json")()
    orders = Order.objects.filter(customer__id=request.user.id).order_by("-created_time")
    serializer.serialize(orders, relations={'restaurant': {'fields': ('name',)}}, stream=response, ensure_ascii=False)
    return response


def favorite_restaurant(request, id):
    if not request.user.is_authenticated():
        return login_required_response(request)
    response = {}
    profile = request.user.get_profile()
    if request.method == 'POST':
        profile.favorite_restaurants.add(Restaurant.objects.get(id=id))
        profile.save()
        response['status'] = 'OK'
        response['info'] = 'Data saved'
    # is GET needed? How about use /restaurant
    elif request.method == 'GET':
        response['status'] = 'NOK'
        response['info'] = 'GET is not supported'
    return HttpResponse(json.dumps(response, ensure_ascii=False))


def favorite_restaurants(request):
    if not request.user.is_authenticated():
        return login_required_response(request)
    response = HttpResponse()
    profile = request.user.get_profile()
    serializer = serializers.get_serializer("json")()
    #serializer.serialize([profile], relations=('favorite_restaurants',), stream=response)
    serializer.serialize(profile.favorite_restaurants.all(), relations=('favorite_restaurants',), ensure_ascii=False,
        stream=response)
    return response

# View or add an user comment for a restaurant    
def restaurant_rating(request, restaurant_id):
    rid = int(restaurant_id)
    r = Restaurant.objects.get(id=restaurant_id)
    response = HttpResponse()

    if request.method == 'GET':
        id_name_fields = {'fields': ('username',)}
        writeJson(r.get_rating(), response, relations={'user': id_name_fields, })
        return response
    elif request.method == 'POST':
        if not request.user.is_authenticated():
            return login_required_response(request)
        data = json.loads(request.raw_post_data)
        comments = data['comments']
        rating = float(data['rating'])
        averageCost = float(data['average_cost'])
        recommendedDishes = data['recommended_dishes']
        try:
            ri = RestaurantInfo.objects.get(restaurant__id=rid)
            divider = ri.divider
            ri.average_cost = (ri.average_cost * divider + averageCost) / (divider + 1)
            ri.average_rating = (ri.average_rating * divider + rating) / (divider + 1)
            good_rate = 0
            if rating >= 3:
                good_rate = 1
            ri.good_rating_percentage = (ri.good_rating_percentage * divider + good_rate) / (divider + 1)
            ri.divider = divider + 1
        except ObjectDoesNotExist:
            ri = RestaurantInfo()
            ri.restaurant_id = rid
            ri.average_cost = averageCost
            ri.average_rating = rating
            if rating >= 3:
                ri.good_rating_percentage = 1
            else:
                ri.good_rating_percentage = 0
            ri.divider = 1
        for dish_id in recommendedDishes:
            try:
                rd = BestRatingDish.objects.get(dish__id=dish_id)
                rd.times = rd.times + 1
            except ObjectDoesNotExist:
                rd = BestRatingDish()
                rd.times = 1
                rd.restaurant_id = rid
                rd.dish_id = dish_id
            rd.save()
        ri.save()

        rc = Rating()
        rc.rating = rating
        rc.user_id = request.user.id
        rc.restaurant_id = rid
        rc.comments = comments
        rc.time = datetime.now()
        rc.average_cost = averageCost
        rc.save()
        for dish_id in recommendedDishes:
            rc.dishes.add(Dish.objects.get(id=dish_id))
        rc.save()
        return createGeneralResponse('OK', 'Comments committed')
    else:
        raise


def get_restaurant_tags(request):
    return getJsonResponse(RestaurantTag.objects.all())


def get_restaurants_with_tag(request, tag_id):
    tag = RestaurantTag.objects.get(id=tag_id)
    return getJsonResponse(Restaurant.objects.filter(tags=tag))
    #return getJsonResponse(RestaurantTag.objects.get(id=tag_id).restaurant_set.all())


def get_regions(request):
    return getJsonResponse(Region.objects.all())


def get_restaurants_in_region(request, region_id):
    return getJsonResponse(Region.objects.get(id=region_id).restaurant_set.all())

def get_following(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'GET':
        return getJsonResponse(user.get_profile().following.all(), {'user': {'fields': ('username',)}})
    elif request.method == 'POST':
        following_user = User.objects.get(id=request.POST.get('user_id'))
        relationship = Relationship(from_person=user.get_profile(), to_person=following_user.get_profile())
        relationship.save()
        return createGeneralResponse('OK', 'You are now following %s' % following_user)
    else:
        raise


def remove_following(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        following_user = User.objects.get(id=request.POST.get('user_id'))
        relationship = Relationship.objects.get(from_person=user.get_profile(), to_person=following_user.get_profile())
        relationship.delete()
        return createGeneralResponse('OK', 'You are not following %s anymore' % following_user)


def followers(request, user_id):
    user = User.objects.get(id=user_id)
    return getJsonResponse(user.get_profile().followers.all(), {'user': {'fields': ('username',)}})


def get_recommended_following(request, user_id):
    user = User.objects.get(id=user_id)
    return getJsonResponse(user.get_profile().recommended_following.all(), {'user':
                                                                                {'fields': ('username',)}
    })


def messages(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'GET':
        message_type = request.GET.get('type', '0')
        print "message_type: %s" % message_type
        return getJsonResponse(UserMessage.objects.filter(to_person=user.get_profile(), type=message_type))
    elif request.method == 'POST':
        from_person = User.objects.get(id=request.POST.get('from_user_id'))
        text = request.POST.get('message')
        message_type = request.POST.get('type', '0')
        message = UserMessage(from_person=from_person.get_profile(),
            to_person=user.get_profile(),
            message=text,
            timestamp=datetime.now(),
            type=message_type)
        message.save()
        return createGeneralResponse('OK', 'Message sent to %s' % user)
    else:
        raise


def meal_participants(request, meal_id):
    if not request.user.is_authenticated():
        return login_required_response(request)
    user = request.user
    if request.method == 'POST':
        meal = Meal.objects.get(id=meal_id)
        if meal.participants.count() >= meal.max_persons:
            return createGeneralResponse('NOK', "No available seat.")
        if user.get_profile() == meal.host:
            return createGeneralResponse('NOK', "You're the host.")
        if meal.is_participant(user.get_profile()):
            return createGeneralResponse('NOK', "You already joined.")
        meal.participants.add(user.get_profile())
        meal.actual_persons += 1
        meal.save()
        return createGeneralResponse('OK', "You've just joined the meal")
    else:
        raise


def view_or_send_meal_invitations(request, user_id):
    if not request.user.is_authenticated():
        return login_required_response(request)
    user = request.user
    if request.method == 'POST':
        to_user = User.objects.get(id=request.POST.get('to_user_id'))
        meal = Meal.objects.get(id=request.POST.get('meal_id'))
        #if meal.host != user.get_profile():
        #    return createGeneralResponse('NOK',"You're not the host - do we check this?")
        if to_user.get_profile() == meal.host or meal.is_participant(to_user.get_profile()):
            return createGeneralResponse('NOK', "%s already joined." % to_user)
        if MealInvitation.objects.filter(from_person=user.get_profile(), to_person=to_user.get_profile(), meal=meal):
            return createGeneralResponse('NOK', "Invitation sent to %s earlier, no new invitation sent." % to_user)
        i = MealInvitation(from_person=user.get_profile(), to_person=to_user.get_profile(), meal=meal)
        i.save()
        return createGeneralResponse('OK', "Invitation sent to %s" % to_user)
    elif request.method == 'GET':
    #        from_person=user.get_profile()
        return getJsonResponse(user.get_profile().invitation)
    else:
        raise


def accept_or_reject_meal_invitations(request, user_id, invitation_id):
    if not request.user.is_authenticated():
        return login_required_response(request)
    user = request.user
    i = MealInvitation.objects.get(id=invitation_id)

    if request.method == 'POST':
        if i.to_person == user.get_profile():
            if i.status == 0: # PENDING
                accept = request.POST.get("accept").lower()
                if accept == "yes":
                    i.status = 1
                    i.save()
                    return meal_participants(request, i.meal.id)  #createGeneralResponse('OK',"Invitation accepted.")
                else:
                    i.status = 2
                    i.save()
                    return createGeneralResponse('OK', "Invitation rejected.")
            else:
                return createGeneralResponse('NOK',
                    "Can not accept/reject an invitation that was already accepted or rejected")
        else:
            return createGeneralResponse('NOK', "Unauthorized: you are not the receiver of this invitation.")
    elif request.method == 'GET':
        if not i.is_related(user.get_profile()):
            return createGeneralResponse('NOK',
                "Unauthorized: you are not either the sender or receiver of the invitation")
        return getJsonResponse([i])
    else:
        raise
