#coding=utf-8
# Create your views here.
from datetime import datetime
import urlparse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy, reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.response import TemplateResponse
from django.utils.timezone import now
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from eo.forms import DishForm, ImgTestForm,\
    UploadFileForm
from eo.models import Restaurant, RestaurantInfo, Rating, Dish, Order,\
    BestRatingDish, RestaurantTag, Region, ImageTest,\
    Relationship, UserMessage, Meal, MealInvitation
from grubcat.eo.forms import *
import simplejson
import sys
from django.conf import settings


### Meal related views ###
class MealListView(ListView):
    queryset = Meal.objects.order_by("time")
    template_name = "meal/meal_list.html"
    context_object_name = "meal_list"
    #TODO add filter to queyset

### User related views ###
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['next'] = self.get_success_url()
        return context

    def form_valid(self, form):
        response = super(RegisterView, self).form_valid(form)
        user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
        login(self.request, user)
        return response

    def get_success_url(self):
        success_url = self.request.REQUEST.get('next', '')
        netloc = urlparse.urlparse(success_url)[1]
        # Use default setting if redirect_to is empty
        if not success_url:
            success_url = reverse_lazy("index")
        # Heavier security check -- don't allow redirection to a different host.
        elif netloc and netloc != self.request.get_host():
            success_url = reverse_lazy("index")
        return success_url


class UserListView(ListView):
    queryset = User.objects.all()
    template_name = "user/user_list.html"
    context_object_name = "user_list"
    paginate_by = 2

### Order related views ###
class OrderCreateView(CreateView):
    form_class = OrderCreateForm
    template_name = 'order/make_order.html'

    def get_initial(self):
        return {'meal_id': self.kwargs['meal_id']}

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        context['meal'] = Meal.objects.get(pk=self.kwargs['meal_id'])
        return context

    def form_valid(self, form):
        order = form.save(False)
        order.customer = self.request.user.get_profile()
        order.meal_id = form.cleaned_data['meal_id']
        order.status = OrderStatus.CREATED
        order.total_price = order.meal.list_price * order.num_persons
        response = super(OrderCreateView, self).form_valid(form)
        order.meal.join(order)
        return response


class OrderDetailView(DetailView):
    model = Order
    context_object_name = "order"
    template_name = "order/order_detail.html"

    def get_object(self, queryset=None):
        order = super(OrderDetailView, self).get_object()
        if order.customer != self.request.user.get_profile():
            print "user see other's order" #TODO raise an exception
        return order

#restaurant admin related views
class OrderCheckInView(FormView):
    template_name = "restaurant/checkin.html"
    form_class = OrderCheckInForm

    def form_valid(self, form):
        code = form.cleaned_data['code']
        order = Order.objects.filter(code=code)

        #TODO uncomment this below
        if order:
            order = order[0]
            #        if order and order[0].meal.restaurant == self.request.user.restaurant:
        #            order = order[0]
        #        else:
        #            order = None
        return render_to_response("restaurant/checkin_result.html", {'order': order})


def use_order(request):
    '''用户就餐时，餐厅管理员标记订单为已使用'''
    if request.method == 'POST':
        code = request.POST.get('code')
        order_id = request.POST.get('id')
        order = Order.objects.get(id=order_id, code=code)
        order.completed_time = now()
        order.status = OrderStatus.USED
        order.save()
        return createSucessJsonResponse('使用订单成功')


def add_dish_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category-name')
        category = DishCategory.objects.get_or_create(name=category_name, restaurant_id=request.user.restaurant.id)
        return createSucessJsonResponse('成功', {'id': category[0].id, 'name': category[0].name, 'created': category[1]})


class DishListView(ListView):
    template_name = "restaurant/dish.html"
    context_object_name = "dish_list"

    def get_queryset(self):
        return Dish.objects.filter(restaurant=self.request.user.restaurant)


class DishCreateView(CreateView):
    form_class = DishForm
    template_name = "restaurant/dish_add_edit.html"
    success_url = reverse_lazy("restaurant_dish_list")

    def get_form_kwargs(self):
        kwargs = super(DishCreateView, self).get_form_kwargs()
        kwargs.update({"restaurant": self.request.user.restaurant})
        return kwargs

    def form_valid(self, form):
        dish = form.save(False)
        dish.restaurant = self.request.user.restaurant
        super(DishCreateView, self).form_valid(form)
        content = r'<a class="auto-close" href="%s"></a>' % reverse_lazy('restaurant_dish_list')
        return HttpResponse(content=content)


class DishUpdateView(UpdateView):
    form_class = DishForm
    model = Dish
    template_name = "restaurant/dish_add_edit.html"
    success_url = reverse_lazy("restaurant_dish_list")

    def form_valid(self, form):
        super(DishUpdateView, self).form_valid(form)
        content = r'<a class="auto-close" href="%s"></a>' % reverse_lazy('restaurant_dish_list')
        return HttpResponse(content=content)

    def get_form_kwargs(self):
        kwargs = super(DishUpdateView, self).get_form_kwargs()
        kwargs.update({"restaurant": self.request.user.restaurant})
        return kwargs


class DishDeleteView(DeleteView):
    model = Dish
    form_class = DishForm
    context_object_name = "dish"
    template_name = "restaurant/dish_confirm_delete.html"
    success_url = reverse_lazy("restaurant_dish_list")

    def get_object(self):
        dish = get_object_or_404(Dish, pk=self.kwargs['pk'],
            restaurant=self.request.user.restaurant)
        return dish

    def delete(self, request, *args, **kwargs):
        super(DishDeleteView, self).delete(request, *args, **kwargs)
        content = r'<a class="auto-close" href="%s"></a>' % reverse_lazy('restaurant_dish_list')
        return HttpResponse(content=content)


def add_menu(request):
    '''添加一个套餐'''
    if request.method == 'GET':
        categories = DishCategory.objects.filter(dish__restaurant=request.user.restaurant).order_by("-id").distinct()

        for cat in categories:
            cat.my_dishes = cat.dish_set.filter(restaurant=request.user.restaurant)

        #        existNoneCategory = False
        #        for cat in categories_id_list:
        #            if None in cat:
        #                existNoneCategory = True
        #                break
        dishes_with_no_category = Dish.objects.filter(restaurant=request.user.restaurant,
            categories__isnull=True).order_by("-id")
        categories_with_no_dish = DishCategory.objects.filter(restaurant=request.user.restaurant,
            dish__isnull=True).order_by("-id")

        #    return render_to_response("restaurant/menu.html", {'dishes': dishes, 'categories': categories,'existNoneCategory':existNoneCategory})
        category_form = DishCategoryForm()
    return render_to_response("restaurant/menu.html", {'categories': categories, 'category_form': category_form,
                                                       'dishes_with_no_category': dishes_with_no_category,'categories_with_no_dish':categories_with_no_dish})


def writeJson(qs, response, relations=None):
    json_serializer = serializers.get_serializer("json")()
    if relations:
        return json_serializer.serialize(qs, ensure_ascii=False, relations=relations, stream=response)
    return json_serializer.serialize(qs, ensure_ascii=False, stream=response)


def getJsonResponse(qs, relations=None):
    response = HttpResponse(content_type='application/json')
    writeJson(qs, response, relations)
    return response

# Create a general response with status and message)
def createGeneralResponse(status, message, extra_dict=None):
    response = {}
    response['status'] = status
    response['info'] = message
    if extra_dict:
        response.update(extra_dict)
    return HttpResponse(simplejson.dumps(response))

# Create a general response with status and message)
def creatJsonResponse(status, message, extra_dict=None):
    response = {'status': status, 'message': message}
    if extra_dict:
        response.update(extra_dict)
    return HttpResponse(simplejson.dumps(response), content_type='application/json', )

# Create a general response with status and message)
def createSucessJsonResponse(message, extra_dict=None):
    return creatJsonResponse('ok', message, extra_dict)

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
        return simplejson.loads(serializer.serialize(query_set, relations=relations))
    return simplejson.loads(serializer.serialize(query_set))


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
    response.write(simplejson.dumps(jsonR, ensure_ascii=False))
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

#
#def get_menu(request):
#    response = HttpResponse()
#    restaurant = Restaurant.objects.get(id=request.GET.get('id'))
#
#    menu = restaurant.menu
#    jsonMenu = simplejson.loads(serializers.serialize('json', [menu]))[0]
#
#    categories = menu.categories.all()
#    jsonCategories = simplejson.loads(serializers.serialize('json', categories))
#    jsonMenu['categories'] = jsonCategories
#
#    dishes = restaurant.dish_set.all() #Dish.objects.filter(restaurant_id=restaurant.id)
#    jsonDishes = simplejson.loads(
#        serializers.serialize('json', dishes, excludes=('restaurant'), relations=('tags', 'categories',)))
#    jsonMenu['dishes'] = jsonDishes
#
#    response.write(simplejson.dumps(jsonMenu, ensure_ascii=False))
#    return response


def login_required_response(request):
    response = {"status": "NOK", "info": "You were not logged in"}
    return HttpResponse(simplejson.dumps(response))


#@transaction.commit_manually
#def make_order(request):
#    if not request.user.is_authenticated():
#        return login_required_response(request)
#    response = {}
#    try:
#        data = simplejson.loads(request.raw_post_data)
#        order = Order()
#        order.restaurant_id = data["restaurant_id"]
#        order.num_persons = data["num_persons"]
#        order.table = data["table_name"]
#        dishes = data["dishes"]
#        totalPrice = 0
#        for dish in dishes:
#            dish_id = dish["dish_id"]
#            print "got one dish id: %s" % dish_id
#            print "quantity: %s" % dish["quantity"]
#            quantity = dish["quantity"]
#            d = Dish.objects.get(id=dish_id)
#            totalPrice = totalPrice + d.price * Decimal(str(quantity))
#        order.total_price = totalPrice
#        order.created_time = datetime.now()
#        order.confirmed_time = datetime.now()
#        order.status = ORDER_STATUS.CREATED # Confirmed
#        order.customer_id = request.user.get_profile().id
#        order.save()
#        #        for dish in dishes:
#        #            dish_id = dish["dish_id"]
#        #            quantity = dish["quantity"]
#        #            od = OrderDishes()
#        #            od.order_id = order.id
#        #            od.dish_id = dish_id
#        #            od.quantity = quantity
#        #            od.save()
#        order.save()
#        transaction.commit()
#    except:
#        print "Unexpected error:", sys.exc_info()
#        transaction.rollback()
#        raise
#    response['status'] = 'OK'
#    response['info'] = "Order confirmed, total price: %s" % totalPrice
#    return HttpResponse(simplejson.dumps(response))


def order_last_modified(request, order_id):
    return Order.objects.get(id=order_id).confirmed_time

#@condition(last_modified_func=order_last_modified)
def get_order_by_id(request, order_id):
    print request.GET.get('ETag')
    if not request.user.is_authenticated():
        return login_required_response(request)
    response = HttpResponse()
    # TODO check if the user has permission to view the order
    serializer = serializers.get_serializer("json")()
    order = Order.objects.get(id=order_id)
    jsonOrder = simplejson.loads(serializer.serialize([order], relations={'restaurant': {'fields': ('name',)}}))[0]
    orderDishes = OrderDishes.objects.filter(order__id=order_id)
    jsonOrderDishes = serializer.serialize(orderDishes, relations=('dish',))
    jsonOrder['fields']['dishes'] = simplejson.loads(jsonOrderDishes)
    response.write(simplejson.dumps(jsonOrder, ensure_ascii=False))
    return response


def get_orders(request):
    if not request.user.is_authenticated():
        return login_required_response(request)
    response = HttpResponse()
    serializer = serializers.get_serializer("json")()
    orders = Order.objects.filter(customer__id=request.user.id).order_by("-created_time")
    serializer.serialize(orders, relations={'restaurant': {'fields': ('name',)}}, stream=response, ensure_ascii=False)
    return response

# get detailed information including dishes of all of the orders, not used by now
def get_orders_detailed(request):
    if not request.user.is_authenticated():
        return login_required_response(request)
    response = HttpResponse()
    serializer = serializers.get_serializer("json")()
    orders = Order.objects.filter(customer__id=request.user.id)
    jsonOrders = []
    jsonOrders = simplejson.loads(serializer.serialize(orders, relations={'restaurant': {'fields': ('name',)}}))
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
    return HttpResponse(simplejson.dumps(response, ensure_ascii=False))


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
        data = simplejson.loads(request.raw_post_data)
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


'''For TEST only'''

def img_test(request):
    if request.method == 'POST':
        form = ImgTestForm(request.POST, request.FILES)
        #if form.is_valid():
        handle_uploaded_image(request.FILES['image'])
        return createGeneralResponse('OK', 'File uploaded')
    else:
        form = ImgTestForm()
        img_test = ImageTest.objects.get(id=2)
    return render_to_response('test/img_test.html', {'img_test': img_test, })


def handle_uploaded_image(file):
    it = ImageTest()
    it.image = file
    it.save()

#    temp use
def handle_uploaded_app(file):
    destination = open(settings.MEDIA_ROOT + '/apps/' + file.name, 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()


def upload_app(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        #if form.is_valid():
        handle_uploaded_app(request.FILES['file'])
        return createGeneralResponse('OK', 'File uploaded')
    else:
        form = UploadFileForm()
    return render_to_response('test/upload.html', {'form': form})


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


def get_user_profile(request, user_id):
    return getJsonResponse([User.objects.get(id=user_id).get_profile()],
            {'user': {'fields': ('username',)},
             'location': {'fields': ('lat', 'lng', 'updated_at')}})


def get_meals(request):
    return getJsonResponse(Meal.objects.filter(time__gte=datetime.now()), ('restaurant', 'host', 'participants'))


def get_meal(request, meal_id):
    if request.method == 'GET':
        meal = Meal.objects.get(id=meal_id)
        return getJsonResponse([meal], ('restaurant', 'host', 'participants'))


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
