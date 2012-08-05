from datetime import datetime

from django.conf.urls.defaults import url
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError
from django.http import HttpResponse
from eo.models import UserProfile, Restaurant, RestaurantTag, Region, \
    RestaurantInfo, Rating, BestRatingDish, Dish, DishCategory, Order, Relationship, \
    UserMessage, Meal, MealInvitation, UserLocation, MealComment, UserTag
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
import simplejson
from taggit.models import Tag
import logging

logger = logging.getLogger(__name__)


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

#todo maybe we can use decorator
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

class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        filtering = {'name': ALL}
        
class UserTagResource(ModelResource):
    class Meta:
        queryset = UserTag.objects.all()
                
class UserResource(ModelResource):
    user = fields.ForeignKey(DjangoUserResource, 'user', full=True)
    orders = fields.ToManyField('eo.apis.OrderResource', 'orders')
    from_user = fields.ToManyField('eo.apis.RelationshipResource', 'from_user')
    location = fields.ToOneField(UserLocationResource, 'location', full=True, null=True)
    following = fields.ToManyField('self', 'following', null=True)
    
    def mergeOneToOneField(self, bundle, field_name, exclude_fields=None):
        if bundle.data[field_name]:
            for key in bundle.data[field_name].data:
                if key == "id": #never ever combine ids as there should be only one, which is the one from UserResource
                    continue
                bundle.data[key] = bundle.data[field_name].data[key]
            del bundle.data[field_name]
    
    def dehydrate(self, bundle):
        self.mergeOneToOneField(bundle, 'user', id)
        self.mergeOneToOneField(bundle, 'location')
        return bundle
    
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/favorite%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_favorite'), name="api_get_favorite"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/order%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_order'), name="api_get_order"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/following/(?P<following_user_id>\d+)%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('following_detail'), name="api_following_detail"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/following%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_following'), name="api_get_following"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/followers%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_followers'), name="api_get_followers"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/following/recommendations%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_recommended_following'), name="api_get_recommended_following"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/messages%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_messages'), name="api_get_messages"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/invitation%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_invitation'), name="api_get_invitation"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/meal%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_meal'), name="api_get_meal"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/feeds%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_feeds'), name="api_get_feeds"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/tags%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_tags'), name="api_get_tags"),    
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/recommendations%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_recommendations'), name="api_get_recommendations"),   
        ]
    
    def obj_update(self, bundle, request=None, **kwargs):
        """
        A quick and dirty fix as tastypie seems to have problems with even simple PATCH request.
        By overwritting this method, PUT request may not work, and any PATCH request that tries to update foreign keys or m2m relations will not work either.
        Hope this will be a new version of tastypie, or we shall use a complete new rest framework.  
        """
        bundle = self.full_hydrate(bundle)
        self.save_related(bundle)
        bundle.obj.save()
        return bundle
    
    def get_favorite(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        restaurant_resource = RestaurantResource()
        return get_my_list(restaurant_resource, obj.favorite_restaurants.all(), request)
    
    def get_order(self, request, **kwargs):
        if not request.user.is_authenticated():
            return login_required(request)
        user_profile = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        order_resource = OrderResource()

        if request.method == 'POST':
            order = Order()
            order.meal = Meal.objects.get(id=request.POST.get('meal_id'))
            order.num_persons = int(request.POST.get('num_persons'))
            order.customer = user_profile
            order.total_price = request.POST.get('total_price')
            order.created_time = datetime.now()
            order.meal.join(order)
            return createGeneralResponse('OK', "You've just joined the meal",{"code":order.code})
        else:
            return order_resource.get_list(request, customer=user_profile)
    
    def get_following(self, request, **kwargs):
        if not request.user.is_authenticated():
            return login_required(request)
        
        me = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))        
        if request.method == 'POST':
            user_to_be_followed = User.objects.get(id=request.POST.get('user_id'))
            relationship = Relationship(from_person=me, to_person=user_to_be_followed.get_profile())
            relationship.save()
            return createGeneralResponse('OK', 'You are now following %s' % user_to_be_followed)
        else:
            obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
            return get_my_list(self, obj.following.all(), request) 
        
    def get_feeds(self, request, **kwargs):
        if not request.user.is_authenticated():
            return login_required(request)
        
        me = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))        
        if request.method == 'GET':
            return get_my_list(OrderResource(), me.feeds, request) 
        else:
            raise
    
    def following_detail(self, request, **kwargs):
        if not request.user.is_authenticated():
            return login_required(request)
        to_person_id = kwargs['following_user_id']
        del(kwargs['following_user_id'])
        me = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))        
        if request.method == 'DELETE':
            user_to_be_not_followed = User.objects.get(id=to_person_id)
            relationship = Relationship.objects.get(from_person=me, to_person=user_to_be_not_followed.get_profile()) 
            relationship.delete()
            return createGeneralResponse('OK', 'You are not following %s anymore' % user_to_be_not_followed)
        else:
            raise
        
    def get_followers(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        return get_my_list(self, obj.followers.all(), request) 
    
    def get_recommended_following(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        return get_my_list(self, obj.recommended_following.all(), request) 
    
    def get_messages(self, request, **kwargs):
        if not request.user.is_authenticated():
            return login_required(request)
        
        to_person = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))        
        if request.method == 'POST':
            from_person = request.user.get_profile()
            text = request.POST.get('message')
            message_type = request.POST.get('type', '0')
            message = UserMessage(from_person=from_person,
                                  to_person=to_person, 
                                  message=text,
                                  timestamp=datetime.now(), 
                                  type=message_type)
            message.save()
            return createGeneralResponse('OK', 'Message sent to %s' % to_person)
        else:
            message_resource = UserMessageResource()
            return message_resource.get_list(request, to_person=to_person)
    
    def get_invitation(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        return get_my_list(MealInvitationResource(), obj.invitations, request)
    
    def get_meal(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        return get_my_list(MealResource(), obj.meals, request)
    
    def get_tags(self, request, **kwargs):
        if not request.user.is_authenticated():
            return login_required(request)
        
        user = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))        
        if request.method == 'POST':
            if request.POST.get('tags'):
                tags = [token.strip() for token in request.POST.get('tags').split(',')]
                user.tags.set(*tags)
                return createGeneralResponse('OK', 'tags %s set' % tags)
            elif request.POST.get('tag'):
                user.tags.add(request.POST.get('tag'))
                return createGeneralResponse('OK', 'tag %s added' % request.POST.get('tag'))
            else:
                raise
        else:
            return get_my_list(UserTagResource(), user.tags.all(), request) 

    def get_recommendations(self, request, **kwargs):
        if not request.user.is_authenticated():
            return login_required(request)
        user = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))        
        if request.method == 'GET':
            return get_my_list(UserResource(), user.recommendations, request)
        else:
            raise
            
    class Meta:
        authorization = Authorization()
        queryset = UserProfile.objects.all()
        resource_name = 'user'
        filtering = {'from_user':ALL,}
        allowed_methods = ['get', 'post', 'put', 'patch']


class RelationshipResource(ModelResource):
    from_person = fields.ForeignKey(UserProfile, 'from_person')
    to_person = fields.ForeignKey(UserProfile, 'to_person')
    
    class Meta:
        queryset = Relationship.objects.all()
        filtering = {'from_person': ALL_WITH_RELATIONS,
                     'to_person': ALL_WITH_RELATIONS,}

class DishCategoryResource(ModelResource):
    class Meta:
        queryset = DishCategory.objects.all()       
        
class DishResource(ModelResource):
    categories = fields.ToManyField(DishCategoryResource, 'categories', full=True, null=True)
    class Meta:
        queryset = Dish.objects.all()
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
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/rating%s$" % (self._meta.resource_name, trailing_slash()),
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
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/restaurant%s$" % (self._meta.resource_name, trailing_slash()),
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

#class MenuResource(ModelResource):
#    categories = fields.ToManyField('eo.apis.DishCategoryResource', 'categories', full=True)
#    dishes = fields.ToManyField('eo.apis.DishResource', 'dishes', full=True)
#    class Meta:
#        queryset = Menu.objects.all()

       
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
    photo = Base64FileField("photo")
    likes = fields.ToManyField(UserResource, 'likes', full=True)
    
    def hydrate(self, bundle):
        bundle.data['actual_persons']=1
        if not bundle.data.get('max_persons'):
            bundle.data['max_persons'] = bundle.data['min_persons']
        return bundle
    
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/comments%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_comments'), name="api_get_comments"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/likes%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('like'), name="api_like"),
        ]
    
    def get_comments(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        meal_comment_resource = MealCommentResource()
        return get_my_list(meal_comment_resource, obj.comments.all(), request)
           
    def like(self, request, **kwargs):
        meal = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        
        if not request.user.is_authenticated():
            return login_required(request)

        user = request.user
        if request.method == 'POST':
            if meal.liked(user.get_profile()):
                return createGeneralResponse('NOK', "You've already liked")
            meal.likes.add(user.get_profile())
            meal.save()
            return createGeneralResponse('OK', "Thank you for liking this meal")
        elif request.method == 'DELETE':
            if meal.liked(user.get_profile()):
                meal.likes.remove(user.get_profile())
                meal.save()
            return createGeneralResponse('OK', "You don't like the meal anymore")
        else:
            raise
    
    class Meta:
        queryset = Meal.objects.all()
        filtering = {'type': ALL,'time':ALL}
        allowed_methods = ['get','post']
        authorization = Authorization()
        ordering = ['time']

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

class OrderResource(ModelResource):        
    meal = fields.ForeignKey(MealResource,'meal', full=True)
    customer = fields.ToOneField(UserResource, 'customer', full=True)
        
    class Meta:
        queryset = Order.objects.all() # .exclude(status=4)
        filtering = {'customer':ALL,}
        ordering = ['created_time','meal']
            
#class CreateUserResource(ModelResource):
#    def obj_create(self, bundle, request=None, **kwargs):
#        weibo_id = bundle.data['weibo_id']
#        username, password=bundle.data.get('username'), bundle.data.get('password')
#        if weibo_id:
#            username,password='weibo_%s' % weibo_id, User.objects.make_random_password()
#        try:
#            user = User.objects.create_user(username, '', password)
#            bundle.obj = user
#            user_profile = user.get_profile()
#            if weibo_id:
#                user_profile.weibo_id = weibo_id
#            auth.login(request, user)
#                 
#        except IntegrityError:
#            raise BadRequest('NOK', "That username already exists")
#        return bundle;
#    
#    class Meta:
##        allowed_methods = ['post']
#        object_class = User
##        authentication = Authentication()
##        authorization = Authorization()
#        fields = ['username']


def createLoggedInResponse(loggedInuser):
    user_resource = UserResource()
    ur_bundle = user_resource.build_bundle(obj=loggedInuser.get_profile())
    serialized = user_resource.serialize(None, user_resource.full_dehydrate(ur_bundle),  'application/json')
    dic = simplejson.loads(serialized)
    dic['status'] = 'OK'
    dic['info'] = "You've logged in"
    return HttpResponse(simplejson.dumps(dic), content_type ='application/json')
            
def mobile_user_register(request):
    if request.method == 'POST':
        username, password=request.POST.get('username'), request.POST.get('password')
        try:
            user = User.objects.create_user(username, '', password)
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return createLoggedInResponse(user)
        except IntegrityError:
            return createGeneralResponse('NOK', "That username already exists")
    else:
        raise # not used by mobile client     

def weibo_user_login(request):
    if request.method == 'POST':
        access_token = request.POST.get('access_token')
        weibo_id = request.POST.get('weibo_id')
        if request.user.is_authenticated():
            # a logged in user, could be logged in as an ordinary user which has no weibo account set, so set weibo account
            # next time when the user logs in as a weibo user, we will know which user who he really is
            user_profile = request.user.get_profile()
            user_profile.weibo_id = weibo_id
            user_profile.weibo_access_token = access_token
            user_profile.save()
            return createLoggedInResponse(request.user)
        else:
            # not logged in, logs the user in as he has been authenticated by weibo at the mobile client side already. 
            # a new uesr might be created if this is the first time the user logs in, check WeiboAuthenticationBackend
            post_dict = dict(request.POST.items()) # POST.dict() is available since django 1.4
            user_to_authenticate = auth.authenticate(**post_dict)
            auth.login(request, user_to_authenticate)
            return createLoggedInResponse(user_to_authenticate)
    else:
        raise # not used by mobile client   
       
def mobile_user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            user_resource = UserResource()
            ur_bundle = user_resource.build_bundle(obj=user.get_profile())
            serialized = user_resource.serialize(None, user_resource.full_dehydrate(ur_bundle),  'application/json')
            dic = simplejson.loads(serialized)
            dic['status'] = 'OK'
            dic['info'] = "You've logged in"
            return HttpResponse(simplejson.dumps(dic), content_type ='application/json')
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
#v1_api.register(MenuResource())
v1_api.register(DishCategoryResource())
v1_api.register(OrderResource())
v1_api.register(RelationshipResource())
v1_api.register(MealResource())
v1_api.register(MealInvitationResource())
v1_api.register(UserLocationResource())
#v1_api.register(OrderDishesResource())
v1_api.register(MealCommentResource())
v1_api.register(TagResource())
v1_api.register(UserTagResource())