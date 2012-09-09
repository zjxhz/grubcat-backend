#coding=utf-8
# Create your views here.
from datetime import datetime
import urlparse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse_lazy, reverse_lazy, reverse
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
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
from eo.view_utils import *
from grubcat.eo.forms import *
import simplejson
import sys
from django.conf import settings

###Menu related views ###
class MenuListView(ListView):
    template_name = "meal/get_menu.html"
    context_object_name = "menu_list"

    def get_queryset(self):
        #TODO filter by  date and time
        num_persons = self.request.GET.get("num_persons", 8)
        qs = Menu.objects.filter(status=MenuStatus.PUBLISHED, num_persons=num_persons).select_related('restaurant', )
        if hasattr(self.request.user, 'restaurant'):
            #餐厅用户只显示本餐厅的菜单
            qs = Menu.objects.filter(restaurant=self.request.user.restaurant, status=MenuStatus.PUBLISHED,
                num_persons=num_persons).select_related('restaurant', )
        return qs


### Meal related views ###
class MealCreateView(CreateView):
    form_class = MealForm
    template_name = 'meal/create_meal.html'

    def get_success_url(self):
        if self.object.status == MealStatus.PUBLISHED:
            return super(MealCreateView, self).get_success_url()
        else:
        #普通用户发起饭聚后需要支付
            return reverse_lazy('create_order', kwargs={'meal_id': self.object.id})

    def form_valid(self, form):
        meal = form.save(False)
        meal.host = self.request.user.get_profile()
        meal.max_persons = meal.min_persons
        menu_id = form.cleaned_data['menu_id']
        if menu_id:
            meal.menu_id = menu_id
            meal.list_price = meal.menu.average_price
            meal.region = None
            #TODO to remove
            meal.restaurant = meal.menu.restaurant

        if hasattr(self.request.user, 'restaurant'):
            meal.status = MealStatus.PUBLISHED
        elif menu_id:
            meal.status = MealStatus.CREATED_WITH_MENU
        else:
            meal.status = MealStatus.CREATED_NO_MENU
        response = super(MealCreateView, self).form_valid(form)
        return response


class MealListView(ListView):
    queryset = Meal.objects.filter(status=MealStatus.PUBLISHED, privacy=MealPrivacy.PUBLIC).order_by("start_date",
        "start_time")
    template_name = "meal/meal_list.html"
    context_object_name = "meal_list"
    #TODO add filter to queyset


class MealDetailView(DetailView):
    model = Meal
    context_object_name = "meal"
    template_name = "meal/meal_detail.html"
    queryset = Meal.objects.select_related('menu__restaurant', 'host__user').prefetch_related('participants__user')

    def get_object(self, queryset=None):
        meal = super(MealDetailView, self).get_object()
        return meal

### group related views ###
class GroupListView(ListView):
#    TODO order by member num
    queryset = Group.objects.filter(privacy=GroupPrivacy.PUBLIC).select_related('category').annotate(
        num_members=Count('members')).order_by('-num_members')
    template_name = "group/group_list.html"
    context_object_name = "group_list"

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)
        context['categories'] = GroupCategory.objects.all()
        return context


class GroupCreateView(CreateView):
    form_class = GroupForm
    template_name = 'group/add_group.html'

    def form_valid(self, form):
        group = form.save(False)
        group.owner = self.request.user
        super(GroupCreateView, self).form_valid(form)
        group.members.add(self.request.user)
        #        TODO need save many to many?
        content = r'<a class="auto-close" href="%s"></a>' % reverse_lazy('group_detail', kwargs={'pk': group.id})
        return HttpResponse(content=content)


class GroupUpdateView(UpdateView):
    form_class = GroupForm
    model = Group
    template_name = "group/edit_group.html"


class GroupLogoUpdateView(UpdateView):
    form_class = GroupLogoForm
    model = Group
    template_name = "group/edit_group_logo.html"

    def form_valid(self, form):
        group = form.save(False)
        super(GroupLogoUpdateView, self).form_valid(form)
        content = r'<a class="auto-close" href="%s"></a>' % reverse_lazy('group_detail', kwargs={'pk': group.id})
        return HttpResponse(content=content)

GROUP_COMMENT_PAGINATE_BY = 5

class GroupDetailView(DetailView):
    model = Group
    context_object_name = "group"
    template_name = "group/group_detail.html"

    def get_queryset(self):
        return Group.objects.prefetch_related('comments__from_person', 'comments__replies__from_person')

    def get_context_data(self, **kwargs):
        parent_comments = GroupComment.objects.filter(parent__isnull=True, group=self.get_object()).select_related(
            'from_person__user').prefetch_related('replies__from_person__user').order_by('-id')
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        context.update({
            "parent_comments":parent_comments[:GROUP_COMMENT_PAGINATE_BY],
            'has_next':parent_comments > GROUP_COMMENT_PAGINATE_BY
        })
        return context

class GroupCommentListView(ListView):
    template_name = "group/comment_list.html"
    context_object_name = "parent_comments"
    model = GroupComment
    paginate_by = GROUP_COMMENT_PAGINATE_BY

    def get_queryset(self):
        parent_comments = GroupComment.objects.filter(parent__isnull=True, group=self.kwargs['group_id']).select_related(
            'from_person__user').prefetch_related('replies__from_person__user').order_by('-id')
        return parent_comments

    def get_context_data(self, **kwargs):
        context = super(GroupCommentListView, self).get_context_data(**kwargs)
        context.update({
            "group_id":self.kwargs['group_id']
        })
        return context

def join_group(request, pk):
    if request.method == 'POST':
        group = Group.objects.get(pk=pk)
        if group.privacy == GroupPrivacy.PUBLIC:
            if request.user not in group.members.all():
                group.members.add(request.user)
                return createSucessJsonResponse(u'已经成功加入该圈子！', {'redirect_url': reverse('group_list')})
            else:
                return createFailureJsonResponse(u'对不起您已经加入该圈子，无需再次加入！')
        else:
        #            need to handle invitation
            return create_no_right_response(u'对不起，只有受到邀请的用户才可以加入该私密圈子')
    elif request.method == 'GET':
        return HttpResponse(u'不支持该操作')


def leave_group(request, pk):
    if request.method == 'POST':
        group = Group.objects.get(pk=pk)
        if request.user in group.members.all():
            group.members.remove(request.user)
            return createSucessJsonResponse(u'已经成功离开该圈子！')
        else:
            return createFailureJsonResponse(u'对不起您还未加入该圈子！')
    elif request.method == 'GET':
        return HttpResponse(u'不支持该操作')


def create_group_comment(request):
    if request.method == 'POST':
        form = GroupCommentForm(request.POST)
        #TODO some checks
        if form.is_valid():
            comment = form.save()
            t = render_to_response('group/new_parent_comment.html', {'comment': comment},
                context_instance=RequestContext(request))
            return createSucessJsonResponse(u'已经成功创建评论！', {'comment_html': t.content})
        else:
            return createFailureJsonResponse(u'对不起您还未加入该圈子！')
    elif request.method == 'GET':
        return HttpResponse(u'不支持该操作')


def del_group_comment(request, pk):
    if request.method == 'POST':
        user_id = request.user.get_profile().id
        comment = GroupComment.objects.filter(pk=pk)
        #TODO some checks
        if len(comment) == 1:
            comment[0].delete()
        return createSucessJsonResponse(u'已经成功删除评论！')
    elif request.method == 'GET':
        return HttpResponse(u'不支持该操作')

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
    template_name = 'order/create_order.html'

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
        meal = order.meal
        if order.customer == meal.host:
            #创建饭聚后，支付
            if meal.status is MealStatus.CREATED_NO_MENU:
                meal.status = MealStatus.PAID_NO_MENU
            elif meal.status is MealStatus.CREATED_WITH_MENU:
                meal.status = MealStatus.PUBLISHED
        order.meal.join(order)
        return response


class OrderDetailView(DetailView):
    model = Order
    context_object_name = "order"
    template_name = "order/order_detail.html"
    queryset = Order.objects.select_related('meal__menu__restaurant')

    def get_object(self, queryset=None):
        order = super(OrderDetailView, self).get_object()
        if order.customer != self.request.user.get_profile():
            print "user see other's order" #TODO raise an exception
        return order

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


def login_required_response(request):
    response = {"status": "NOK", "info": "You were not logged in"}
    return HttpResponse(simplejson.dumps(response))


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
