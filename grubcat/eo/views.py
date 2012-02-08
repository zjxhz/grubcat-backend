# Create your views here.
from django.http import HttpResponse
from grubcat.eo.models import *
from django.core import serializers
from django.db.models.query import QuerySet
import logging
import simplejson
import sys
from django.shortcuts import render_to_response
from django.contrib import auth
from datetime import datetime
from django.db import transaction
from decimal import Decimal


def hello(request):
    return HttpResponse("Hello world")

# use this maybe only for get_menu? for more common one, use writeJson
def getJsonResponse(qs, response, useNatureKeys=False):
    json_serializer = serializers.get_serializer("json")()
    json_serializer.serialize(qs, ensure_ascii=False, stream=response, use_natural_keys=useNatureKeys)
    from django.forms.models import model_to_dict
    for intance in qs:
        print model_to_dict(intance)
    return response

def writeJson(qs, response):
    json_serializer = serializers.get_serializer("json")()
    return json_serializer.serialize(qs, ensure_ascii=False, stream=response)

# get distance in meter, code from google maps
def getDistance( lng1,  lat1,  lng2,  lat2):
    EARTH_RADIUS = 6378.137
    from math import asin,sin,cos,acos,radians, degrees,pow,sqrt, hypot,pi
    radLat1 = radians(lat1) 
    radLat2 = radians(lat2) 
    a = radLat1 - radLat2
    b = radians(lng1) - radians(lng2)
    s = 2 * asin(sqrt(pow(sin(a/2),2) + cos(radLat1)*cos(radLat2)*pow(sin(b/2),2)))
    s = s * EARTH_RADIUS
    return s*1000

def restaurantList(request):
    response = HttpResponse()
    key = request.GET.get('key')
    if key:
        return getJsonResponse(Restaurant.objects.filter(name__contains=key), response)
    return getJsonResponse(Restaurant.objects.all(), response)

def get_restaurant(request, id):
    response = HttpResponse()
    writeJson(Restaurant.objects.filter(id=id), response)
    return response
    
def get_restaurant_list_by_geo(request):
    try:
        response = HttpResponse()
        lng = float(request.GET.get('longitude'))
        lat = float(request.GET.get('latitude'))
        rangeInMeter = float(request.GET.get('range'))
        # TODO page...
        rInRange = []
        for r in Restaurant.objects.all():
            if r.longitude and r.latitude:
                if getDistance(lng, lat, r.longitude, r.latitude)  < rangeInMeter:
                    rInRange.append(r)
        qs = Restaurant.objects.filter(id__in=[r.id for r in rInRange])
        writeJson(qs, response)
        #print Restaurant.objects.filter(getDistance(longitude,latitude,lng,lat) < rangeInMeter)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    return  response

def get_menu(request):
    response = HttpResponse()
    restaurant = Restaurant.objects.get(id=request.GET.get('id'))

    menu = restaurant.menu
    jsonMenu = simplejson.loads(serializers.serialize('json', [menu]))[0]
    
    categories = menu.categorydish_set.all()
    jsonCategories = simplejson.loads(serializers.serialize('json', categories))
    jsonMenu['categories']=jsonCategories

    dishes = restaurant.dish_set.all() #Dish.objects.filter(restaurant_id=restaurant.id)
    jsonDishes = simplejson.loads(serializers.serialize('json', dishes, excludes=('restaurant'), relations=('tags','categories',)))
    jsonMenu['dishes']=jsonDishes

    response.write(simplejson.dumps(jsonMenu, ensure_ascii=False))
    return response

def get_menu2(request):
    response = HttpResponse()
    rid = request.GET.get('id')
    qs = Dish.objects.filter(restaurant__id=int(rid))
    return getJsonResponse(qs, response)

def test(request):
    response = HttpResponse()
    qs = B.objects.all()
    return getJsonResponse(qs, response)

def user_login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    response = {}
    if user is not None and user.is_active:
        response['status']='OK'
        response['info']="You've logged in"
        auth.login(request, user)
    else:
        response['status']='NOK'
        response['info']="Incorrect username or password"
    return HttpResponse(simplejson.dumps(response))

def login(request):
    return render_to_response("registration/login.html")

def test_make_order(request):
    return render_to_response("order/make_order.html")

def login_required(request):
    response = {"status":"NOK", "info":"You were not logged in"}
    return HttpResponse(simplejson.dumps(response))

@transaction.commit_manually
def make_order(request):
    if not request.user.is_authenticated():
        return self.login_required(request)
    response = {}
    try:
        data = simplejson.loads(request.raw_post_data)
        order = Order()
        order.restaurant_id = data["restaurant_id"]
        order.num_persons = data["num_persons"]
        order.table = data["table_name"]
        dishes = data["dishes"]
        totalPrice = 0
        for dish in dishes:
            dish_id = dish["dish_id"]
            print "got one dish id: %s" % dish_id
            print "quantity: %s" % dish["quantity"]
            quantity = dish["quantity"]
            d = Dish.objects.get(id=dish_id)
            totalPrice = totalPrice + d.price * Decimal(str(quantity))
        order.total_price = totalPrice
        order.created_time = datetime.now()
        order.confirmed_time = datetime.now()
        order.status = OrderStatus.CONFIRMED # Confirmed
        order.customer_id = request.user.id
        order.save()
        for dish in dishes:
            dish_id = dish["dish_id"]
            quantity = dish["quantity"]
            od = OrderDishes()
            od.order_id = order.id
            od.dish_id = dish_id
            od.quantity = quantity
            od.save()
        order.save()
        transaction.commit()
    except:
        print "Unexpected error:", sys.exc_info()
        transaction.rollback()
        raise
    response['status']='OK'
    response['info']="Order confirmed, total price: %s" % totalPrice     
    return HttpResponse(simplejson.dumps(response))

def get_order_by_id(request, id):
    if not request.user.is_authenticated():
        return login_required(request)
    response = HttpResponse()
    # TODO check if the user has permission to view the order
    serializer = serializers.get_serializer("json")()
    order = Order.objects.get(id=id)
    jsonOrder = simplejson.loads(serializer.serialize([order], relations={'restaurant':{'fields':('name',)}}))[0]
    orderDishes = OrderDishes.objects.filter(order__id=id)
    jsonOrderDishes = serializer.serialize(orderDishes, relations=('dish',))
    jsonOrder['fields']['dishes'] = simplejson.loads(jsonOrderDishes)
    response.write(simplejson.dumps(jsonOrder, ensure_ascii=False))
    return response

def get_orders(request):
    if not request.user.is_authenticated():
        return login_required(request)
    response = HttpResponse()
    serializer = serializers.get_serializer("json")()
    orders = Order.objects.filter(customer__id=request.user.id)
    serializer.serialize(orders, relations={'restaurant':{'fields':('name',)}}, stream=response, ensure_ascii=False)
    return response

# get detailed information including dishes of all of the orders, not used by now
def get_orders_detailed(request):
    if not request.user.is_authenticated():
        return login_required(request)
    response = HttpResponse()
    serializer = serializers.get_serializer("json")()
    orders = Order.objects.filter(customer__id=request.user.id)
    jsonOrders = []
    jsonOrders = simplejson.loads(serializer.serialize(orders, relations={'restaurant':{'fields':('name',)}}))
    for jsonOrder in jsonOrders:
        orderID = jsonOrder['pk']
        orderDishes = OrderDishes.objects.filter(order__id=orderID)
        jsonDishes = []
        for orderDish in orderDishes:
            dish = orderDish.dish
            jsonDish = serializer.serialize([dish])
            jsonDishes.append(simplejson.loads(jsonDish)[0])
        jsonOrder['fields']['dishes'] = jsonDishes
    response.write(simplejson.dumps(jsonOrders, ensure_ascii=False))
    return responset

def get_user_profile(request):
    if not request.user.is_authenticated():
        return login_required(request)
    response = HttpResponse()
    response.write(request.user.get_profile())
    return response

def favorite_restaurant(request, id):
    if not request.user.is_authenticated():
        return login_required(request)
    response = {}
    profile = request.user.get_profile()
    if request.method == 'POST':
        profile.favorite_restaurants.add(Restaurant.objects.get(id=id))
        profile.save()
        response['status']='OK'
        response['info']='Data saved' 
    # is GET needed? How about use /restaurant
    elif request.method == 'GET':
        response['status']='NOK'
        response['info']='GET is not supported' 
    return HttpResponse(simplejson.dumps(response, ensure_ascii=False))
    
def favorite_restaurants(request):
    if not request.user.is_authenticated():
        return login_required(request)
    response = HttpResponse()
    profile = request.user.get_profile()
    serializer = serializers.get_serializer("json")()
    #serializer.serialize([profile], relations=('favorite_restaurants',), stream=response)
    serializer.serialize(profile.favorite_restaurants.all(), relations=('favorite_restaurants',), ensure_ascii=False, stream=response)
    return response
    
