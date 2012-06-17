from datetime import datetime
from decimal import Decimal
from django.conf.urls.defaults import url
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from eo.models import UserProfile, Restaurant, RestaurantTag, Region, \
    RestaurantInfo, Rating, BestRatingDish, Dish, Menu, DishCategory, DishTag, \
    DishOtherUom, Order, Relationship, UserMessage, Meal, MealInvitation, \
    UserLocation, OrderDishes, MealComment
from tastypie import fields
from tastypie.api import Api
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.fields import FileField
from tastypie.paginator import Paginator
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from urllib import urlencode
import base64
import mimetypes
import os
import simplejson


class Base64FileField(FileField):
    """
    A django-tastypie field for handling file-uploads through raw post data. see https://gist.github.com/709890
    It uses base64 for en-/decoding the contents of the file.
    Usage:

    class MyResource(ModelResource):
        file_field = Base64FileField("file_field")
        
        class Meta:
            queryset = ModelWithFileField.objects.all()

    In the case of multipart for submission, it would also pass the filename.
    By using a raw post data stream, we have to pass the filename within our
    file_field structure:

    file_field = {
        "name": "myfile.png",
        "file": "longbas64encodedstring",
        "content_type": "image/png" # on hydrate optional
    }
    """
#    def dehydrate(self, bundle):
#        if not bundle.data.has_key(self.instance_name) and hasattr(bundle.obj, self.instance_name):
#            file_field = getattr(bundle.obj, self.instance_name)
#            if file_field:
#                try:
#                    content_type, encoding = mimetypes.guess_type(file_field.file.name)
#                    b64 = open(file_field.file.name, "rb").read().encode("base64")
#                    ret = {
#                        "name": os.path.basename(file_field.file.name),
#                        "file": b64,
#                        "content-type": content_type or "application/octet-stream"
#                    }
#                    return ret
#                except:
#                    pass
#        return None

    def hydrate(self, obj):
        value = super(FileField, self).hydrate(obj)
        if value:
            value = SimpleUploadedFile(value["name"], base64.b64decode(value["file"]), getattr(value, "content_type", "application/octet-stream"))
        return value
    
'''TODO add a base class that:
    is a sub class of ModelResource
    has method get_my_list, which return a response of a serialized query set
    has method mergeOneToOneField, which merge the fields of the one to one field to self
    use PageNumberPaginator
'''
def get_my_list(resource, queryset, request):
    '''
    Returns serialized list of the queryset, a bit duplicated with get_list(self, request, **kwargs). 
    
    This is useful when the filtering string is difficult to construct
    '''
    base_object_list = resource.apply_authorization_limits(request, queryset)
    sorted_objects = resource.apply_sorting(base_object_list, options=request.GET)

    paginator = resource._meta.paginator_class(request.GET, sorted_objects, 
                                               resource_uri=resource.get_resource_list_uri(),
                                                limit=resource._meta.limit)
    to_be_serialized = paginator.page()

    bundles = [resource.build_bundle(obj=obj, request=request) for obj in to_be_serialized['objects']]
    to_be_serialized['objects'] = [resource.full_dehydrate(bundle) for bundle in bundles]
    to_be_serialized = resource.alter_list_data_to_serialize(request, to_be_serialized)
    return resource.create_response(request, to_be_serialized)

def login_required(request):
    response = {"status": "NOK", "info": "You were not logged in"}
    return HttpResponse(simplejson.dumps(response))

# Create a general response with status and message)
def createGeneralResponse(status, message, extra_dict=None):
    response = {}
    response['status'] = status
    response['info'] = message
    if extra_dict:
        response.update(extra_dict)
    return HttpResponse(simplejson.dumps(response))

class PageNumberPaginator(Paginator):
    def get_offset(self):
        self.offset = self.limit * self.get_page()
        return self.offset

    def get_page(self):
        page = 0
        if 'page' in self.request_data:
            page = int(self.request_data['page'])
        return page
    
    def _generate_uri(self, limit, offset):
        if self.resource_uri is None:
            return None
        request_params = dict([k, v.encode('utf-8')] for k, v in self.request_data.items())
        request_params.update({'limit': limit, 'page': offset/limit})
        return '%s?%s' % (
            self.resource_uri,
            urlencode(request_params)
        )
    
class DjangoUserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'django_user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get']
        include_resource_uri = False

class UserLocationResource(ModelResource):
    class Meta:
        queryset = UserLocation.objects.all()        
        
class UserResource(ModelResource):
    user = fields.ForeignKey(DjangoUserResource, 'user', full=True)
    orders = fields.ToManyField('eo.apis.OrderResource', 'orders')
    from_user = fields.ToManyField('eo.apis.RelationshipResource', 'from_user')
    location = fields.ToOneField(UserLocationResource, 'location', full=True, null=True)
    
    def mergeOneToOneField(self, bundle, field_name):
        if bundle.data[field_name]:
            for key in bundle.data[field_name].data:
                bundle.data[key] = bundle.data[field_name].data[key]
            del bundle.data[field_name]
    
    def dehydrate(self, bundle):
        self.mergeOneToOneField(bundle, 'user')
        self.mergeOneToOneField(bundle, 'location')
        return bundle
    
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/favorite%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_favorite'), name="api_get_favorite"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/order%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_order'), name="api_get_order"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/following%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_following'), name="api_get_following"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/followers%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_followers'), name="api_get_followers"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/following/recommendations%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_recommended_following'), name="api_get_recommended_following"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/messages%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_messages'), name="api_get_messages"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/invitation%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_invitation'), name="api_get_invitation"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/meal%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_meal'), name="api_get_meal"),
        ]
    
    
    def get_favorite(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        restaurant_resource = RestaurantResource()
        return get_my_list(restaurant_resource, obj.favorite_restaurants.all(), request)
    
    def get_order(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        order_resource = OrderResource()
        return order_resource.get_list(request, customer=obj)
    
    def get_following(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        return get_my_list(self, obj.following.all(), request) 
    
    def get_followers(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        return get_my_list(self, obj.followers.all(), request) 
    
    def get_recommended_following(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        return get_my_list(self, obj.recommended_following.all(), request) 
    
    def get_messages(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        message_resource = UserMessageResource()
        return message_resource.get_list(request, to_person=obj)
    
    def get_invitation(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        return get_my_list(MealInvitationResource(), obj.invitations, request)
    
    def get_meal(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        return get_my_list(MealResource(), obj.meals, request)
        
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'user'
        filtering = {'from_user':ALL,}

class RelationshipResource(ModelResource):
    from_person = fields.ForeignKey(UserProfile, 'from_person')
    to_person = fields.ForeignKey(UserProfile, 'to_person')
    
    class Meta:
        queryset = Relationship.objects.all()
        filtering = {'from_person': ALL_WITH_RELATIONS,
                     'to_person': ALL_WITH_RELATIONS,}

class DishCategoryResource(ModelResource):
    parent_category = fields.ForeignKey('self', 'parent_category', null=True, full=True)
    class Meta:
        queryset = DishCategory.objects.all()       
        
class DishTagResrouce(ModelResource):
    class Meta:
        queryset = DishTag.objects.all()
        paginator_class = PageNumberPaginator
        
class DishResource(ModelResource):
    tags = fields.ToManyField(DishTagResrouce, 'tags', full=True)
    other_uom = fields.ToManyField('eo.apis.DishOtherUomResource', 'other_uom', full=True, null=True)
    categories = fields.ToManyField(DishCategoryResource, 'categories', full=True, null=True)
    class Meta:
        queryset = Dish.objects.all()
        paginator_class = PageNumberPaginator

class DishOtherUomResource(ModelResource):
    class Meta:
        queryset = DishOtherUom.objects.all()
        paginator_class = PageNumberPaginator

#TODO what if pagination is needed for comments?              
class RestaurantResource(ModelResource):
    tags = fields.ToManyField('eo.apis.RestaurantTagResource', 'tags')
    regions = fields.ToManyField('eo.apis.RegionResource', 'regions')
    info = fields.ToOneField('eo.apis.RestaurantInfoResource', 'info', full=True, null=True)
    ratings = fields.ToManyField('eo.apis.RatingResource', 'ratings', full=True, null=True)
    best_rating_dishes = fields.ToManyField('eo.apis.BestRatingDishResource', 'best_rating_dishes', full=True, null=True)
    user_favorite = fields.ToManyField('eo.apis.UserResource', 'user_favorite')
    def dehydrate(self, bundle):
        if not bundle.data['info']:
            bundle.data['average_cost'] = -1
            bundle.data['average_rating'] = -1
            bundle.data['good_rating_percentage'] = -1
        else:
            for key in bundle.data['info'].data:
                bundle.data[key] = bundle.data['info'].data[key]
        del bundle.data['regions']
        del bundle.data['tags']
        del bundle.data['info']
        
        return bundle
    
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/rating%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_rating'), name="api_get_rating"),
        ]
    
    def get_rating(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        rating_resource = RatingResource()
        return rating_resource.get_list(request, restaurant=obj)
    
    def getDistance(self, lng1,  lat1,  lng2,  lat2):
        EARTH_RADIUS = 6378.137
        from math import asin,sin,cos,radians, pow,sqrt
        radLat1 = radians(lat1) 
        radLat2 = radians(lat2) 
        a = radLat1 - radLat2
        b = radians(lng1) - radians(lng2)
        s = 2 * asin(sqrt(pow(sin(a/2),2) + cos(radLat1)*cos(radLat2)*pow(sin(b/2),2)))
        s = s * EARTH_RADIUS
        return s*1000

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = {}
        
        if "longitude" in filters:
            lng = float(filters['longitude'])
            lat = float(filters['latitude'])
            rangeInMeter = float(filters['range'])
            restaurants = []
            for r in Restaurant.objects.all():
                if r.longitude and r.latitude:
                    distance = self.getDistance(lng, lat, r.longitude, r.latitude)
                    if distance < rangeInMeter:
                        restaurants.append(r)
            orm_filters["pk__in"] = [r.pk for r in restaurants]
        else:
            orm_filters = super(RestaurantResource, self).build_filters(filters)
        return orm_filters
    
    class Meta:
        queryset = Restaurant.objects.all()
        paginator_class = PageNumberPaginator
        filtering = {
            'name': ALL,         
            'tel': ALL,
            'longitude': ALL,
            'latitude': ALL,
            'tags': ALL_WITH_RELATIONS,
            'regions': ALL_WITH_RELATIONS,
            'user_favorite': ALL_WITH_RELATIONS,
        }

class RestaurantInfoResource(ModelResource):
    restaurant = fields.ForeignKey(RestaurantResource, 'restaurant')
    
    class Meta:
        queryset = RestaurantInfo.objects.all()
        resource_name = 'restaurant_info'
        excludes = ['divider','id',]
        include_resource_uri = False

class RatingResource(ModelResource):
    restaurant = fields.ForeignKey(RestaurantResource, 'restaurant')
    
    class Meta:
        queryset = Rating.objects.all()
        include_resource_uri = False
        filtering = {'restaurant': ALL, }

class BestRatingDishResource(ModelResource):
    dish = fields.ForeignKey(DishResource, 'dish', full=True)
    
    class Meta:
        queryset = BestRatingDish.objects.all()
        
                                
class RestaurantTagResource(ModelResource):
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/restaurant%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_restaurants'), name="api_get_restaurants"),
        ]
    
    def get_restaurants(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        restaurant_resource = RestaurantResource()
        tag = RestaurantTag.objects.get(id=obj.pk)
        return restaurant_resource.get_list(request, tags=tag)
        
    class Meta:
        queryset = RestaurantTag.objects.all()
        resource_name = 'restaurant_tag'
        authorization = Authorization()
        allowed_methods = ['get', 'post', 'delete']
        
class RegionResource(ModelResource):
    class Meta:
        queryset = Region.objects.all()

class MenuResource(ModelResource):
    categories = fields.ToManyField('eo.apis.DishCategoryResource', 'categories', full=True)
    dishes = fields.ToManyField('eo.apis.DishResource', 'dishes', full=True)
    class Meta:
        queryset = Menu.objects.all()

class OrderResource(ModelResource):        
    customer = fields.ToOneField('eo.apis.UserResource', 'customer')
    dishes = fields.ToManyField(DishResource, 'dishes', full=True)
    restaurant = fields.ToOneField(RestaurantResource, 'restaurant')
    #meal = fields.ToOneField('eo.apis.MealResource', 'meal')
    
    def dehydrate(self, bundle):
        for dish in bundle.data['dishes']:
            order_dish = OrderDishes.objects.filter(order=bundle.obj).get(dish=dish.obj)
#            dish.data['dish'] = dish.data
            dish.data['quantity'] = order_dish.quantity
#        del bundle.data['dishes']
        return bundle
        
    class Meta:
        queryset = Order.objects.all()
        filtering = {'customer':ALL,}

class OrderDishesResource(ModelResource):
    order = fields.ForeignKey(OrderResource, 'order')
    dish = fields.ForeignKey(DishResource, 'dish')
    class Meta:
        queryset = OrderDishes.objects.all()
        
class UserMessageResource(ModelResource): 
    from_person = fields.ForeignKey(UserResource, 'from_person', full=True)
    to_person = fields.ForeignKey(UserResource, 'to_person', full=True )
    
    class Meta:
        queryset = UserMessage.objects.all()
        filtering = {'from_person': ALL_WITH_RELATIONS,
                     'to_person': ALL_WITH_RELATIONS,
                     'type':ALL,}

class MealResource(ModelResource):
    restaurant = fields.ForeignKey(RestaurantResource, 'restaurant', full=True)
    host = fields.ForeignKey(UserResource, 'host', full=True)
    participants = fields.ToManyField(UserResource, 'participants', full=True, null=True)
    order = fields.ToOneField('eo.apis.OrderResource', 'order', full=True)
    photo = Base64FileField("photo")
    
    def hydrate(self, bundle):
        bundle.data['actual_persons']=1
        if not bundle.data.get('max_persons'):
            bundle.data['max_persons'] = bundle.data['min_persons']
        bundle.data['order']['created_time'] = datetime.now()
        bundle.data['order']['confirmed_time']=bundle.data['order']['created_time'] 
        bundle.data['order']['status']=2
        bundle.data['order']['customer'] = bundle.data['host']
        bundle.data['order']['restaurant'] = bundle.data['restaurant']
        totalPrice = 0
        for dish_data in bundle.data['order']['dishes']:
            dish = Dish.objects.get(id=dish_data['id'])
            quantity = dish_data["quantity"]
            totalPrice = totalPrice + dish.price * quantity
        bundle.data['order']['total_price']=totalPrice
        return bundle
    
    def save_order_dishes(self, bundle, order):
        for dish_bundle in bundle.data['order']['dishes']:
            dish = Dish.objects.get(id=dish_bundle['id'])
            order_dish=OrderDishes(order=order, dish=dish, quantity=dish_bundle['quantity'])
            order_dish.save()
        order.save()

    def save_related(self, bundle):
        """
        Call the base impl and save additionally the dishes of the order.
        
        Tastypie seems not able to save related objects in a related object, e.g. in order to save a meal, related object
        order should be saved, but order has related objects dishes, too.
        """
        super(MealResource, self).save_related(bundle)
        self.save_order_dishes(bundle, bundle.obj.order)
    
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/comments%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_comments'), name="api_get_comments"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/participants%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('participants'), name="api_participants"),
        ]
    
    def get_comments(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        meal_comment_resource = MealCommentResource()
        return get_my_list(meal_comment_resource, obj.comments.all(), request)
    
    def participants(self, request, **kwargs):
        meal = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        
        if not request.user.is_authenticated():
            return login_required(request)
    
        user = request.user
        if request.method == 'POST':
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
    
    class Meta:
        queryset = Meal.objects.all()
        filtering = {'type': ALL,'time':ALL}
        allowed_methods = ['get','post']
        authorization = Authorization()

class MealCommentResource(ModelResource):
    from_person = fields.ForeignKey(UserResource, 'from_person', full=True)
    meal  = fields.ForeignKey(MealResource, 'meal')
    
    class Meta:
        queryset = MealComment.objects.all()
        filtering= {'meal': ALL}
    
class MealInvitationResource(ModelResource):
    from_person = fields.ForeignKey(UserResource, 'from_person', full=True)
    to_person = fields.ForeignKey(UserResource, 'to_person', full=True)
    meal = fields.ForeignKey(MealResource, 'meal', full=True)
    
    class Meta:
        queryset = MealInvitation.objects.all()
        filtering = {'from_person':ALL_WITH_RELATIONS, 
                     'to_person': ALL_WITH_RELATIONS,
                     }
        resource_name = 'invitation'
        
def mobile_user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return createGeneralResponse('OK', "You've logged in", {"id":user.id})
        else:
            return createGeneralResponse('NOK', "Incorrect username or password")
    else:
        raise # not used by mobile client
    
def mobile_user_logout(request):
    if request.method == 'POST':
        logout(request)
        return createGeneralResponse('OK',"You've logged out.")
        # return HttpResponse("Hello world") # there is no response from the server even the code is so simple, might be bug of dotcloud
        # raise Exception("what's going on here?") # enable this line to check that the code IS executed here
    else:
        raise # not used by mobile client      
v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(DjangoUserResource())
v1_api.register(RestaurantResource())
v1_api.register(RestaurantTagResource())
v1_api.register(RegionResource())
v1_api.register(RestaurantInfoResource())
v1_api.register(RatingResource())
v1_api.register(DishResource())
v1_api.register(MenuResource())
v1_api.register(DishCategoryResource())
v1_api.register(OrderResource())
v1_api.register(RelationshipResource())
v1_api.register(MealResource())
v1_api.register(MealInvitationResource())
v1_api.register(UserLocationResource())
v1_api.register(OrderDishesResource())
v1_api.register(MealCommentResource())