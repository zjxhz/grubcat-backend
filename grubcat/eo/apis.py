#coding=utf-8
from datetime import datetime, timedelta
from django.conf.urls.defaults import url
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponse
from eo.exceptions import NoAvailableSeatsError
from eo.models import UserLocation, UserTag, UserPhoto, UserProfile, \
    MealParticipants, Meal, Relationship, UserMessage, Visitor, Restaurant, \
    DishCategory, DishCategoryItem, MealComment, MealInvitation, Order, Menu
from eo.pay.alipay.alipay import create_app_pay
from tastypie import fields
from tastypie.api import Api
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.http import HttpUnauthorized
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
import json
import logging
import os
import re

logger = logging.getLogger('api')
        
class EOResource(ModelResource):
    def determine_format(self, request):
        return 'application/json'
        
    def get_my_list(self, resource, queryset, request):
        '''
        Returns serialized list of the queryset, a bit duplicated with get_list(self, request, **kwargs). 
        
        This is useful when the filtering string is difficult to construct
        '''
        applicable_filters = resource.build_filters(filters=request.GET.copy())
        if len(applicable_filters.keys()) and hasattr(queryset, 'filter') > 0:
            queryset = queryset.filter(**applicable_filters)
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

    def mergeOneToOneField(self, bundle, field_name, exclude_fields=None):
        if bundle.data[field_name]:
            for key in bundle.data[field_name].data:
                if exclude_fields and key in exclude_fields:
                    continue;
                bundle.data[key] = bundle.data[field_name].data[key]
            del bundle.data[field_name]

        
#todo maybe we can use decorator
def login_required(request):
    response = {"status": "NOK", "info": "You were not logged in"}
    return HttpUnauthorized(json.dumps(response))
         

# Create a general response with status and message)
def createGeneralResponse(status, message, extra_dict=None):
    response = {}
    response['status'] = status
    response['info'] = message
    if extra_dict:
        response.update(extra_dict)
    return HttpResponse(json.dumps(response))

class DjangoUserResource(EOResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'django_user'
        fields = ['username']
        allowed_methods = ['get']
        filtering = {'username': ALL}

class UserLocationResource(EOResource):
    class Meta:
        allowed_methods = ['get']
        queryset = UserLocation.objects.all()
      
        
class UserTagResource(EOResource):
    def override_urls(self):
        return [url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/users%s$" % (self._meta.resource_name, trailing_slash()),
            self.wrap_view('users'), name="api_users"),]
    
    def users(self, request, **kwargs):
        user_tag = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        if request.method == 'GET':
            return self.get_my_list(UserResource(), user_tag.tagged_users(), request )                    
    class Meta:
        queryset = UserTag.objects.all()

class UserPhotoResource(EOResource):
    def post_list(self, request, **kwargs):
        # in a REST framework there is no easy way to delete multiple objects at a time, so just use post here, be careful about the authentication
        deleted_ids = request.POST.get("deleted_ids")
        if deleted_ids:
            UserPhoto.objects.filter(id__in=deleted_ids.split(",")).delete();
            return createGeneralResponse("OK", "Photos deleted")  
        else:
            return super(request, **kwargs)
                          
    def dehydrate(self, bundle):
        bundle.data['thumbnail'] = bundle.obj.photo_thumbnail
        bundle.data['large'] = bundle.obj.large_photo
        return bundle
    
    class Meta:
        queryset = UserPhoto.objects.all()
        authorization = Authorization()
        filtering={"id":ALL}
        allowed_methods = ['get', 'post', 'delete']

class SimpleUserResource(EOResource):
    user = fields.ForeignKey(DjangoUserResource, 'user', full=True)
    location = fields.ToOneField(UserLocationResource, 'location', full=True, null=True)
    def dehydrate(self, bundle):
        if not bundle.data['location']:
            # simulate a location. TODO remove these lines in production
            bundle.data['lat'] = 30.275
            bundle.data['lng'] = 120.148
            bundle.data['updated_at'] = "2013-04-21"
        
        bundle.data['small_avatar'] = bundle.obj.medium_avatar
        bundle.data['big_avatar'] = bundle.obj.big_avatar  
        self.mergeOneToOneField(bundle, 'user', ['id', ])
        self.mergeOneToOneField(bundle, 'location', ['id', ])
        return bundle
    
    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        
        orm_filters = super(SimpleUserResource, self).build_filters(filters)
        if "ids" in filters:
            orm_filters["pk__in"] = str(filters['ids']).split(',')
        return orm_filters
    
    class Meta:
        queryset = UserProfile.objects.all()
        authorization = Authorization()
        resource_name = 'simple_user'

class MealParticipantResource(EOResource):
    user = fields.ForeignKey(SimpleUserResource, 'userprofile', full=True)
    
    def dehydrate(self, bundle):
        self.mergeOneToOneField(bundle, 'user')
        return bundle
        
        
    class Meta:
        queryset = MealParticipants.objects.all()
        
    
class UserResource(EOResource):
    user = fields.ForeignKey(DjangoUserResource, 'user', full=True)
    orders = fields.ToManyField('eo.apis.OrderResource', 'orders')
    from_user = fields.ToManyField('eo.apis.RelationshipResource', 'from_user')
    location = fields.ToOneField(UserLocationResource, 'location', full=True, null=True)
    following = fields.ToManyField('self', 'following', null=True)
    tags = fields.ToManyField(UserTagResource, 'tags', full=True, null=True)
    photos = fields.ToManyField(UserPhotoResource, 'photos', full=True, null=True)
    
    def hydrate(self, bundle):
        bundle.data['avatar'] = str(bundle.obj.avatar) # never change avatar in a patch request, or it always add /media/
        return bundle
        
    def dehydrate(self, bundle):
        if not bundle.data['location']:
            # simulate a location. TODO remove these lines in production
            bundle.data['lat'] = 30.275
            bundle.data['lng'] = 120.148
            bundle.data['updated_at'] = "2012-10-16"
        
        bundle.data['small_avatar'] = bundle.obj.medium_avatar #small is too small for iPhone
        bundle.data['big_avatar'] = bundle.obj.big_avatar  
        self.mergeOneToOneField(bundle, 'user', ['id', ])
        self.mergeOneToOneField(bundle, 'location', ['id', ])
        return bundle
       
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/order%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_order'), name="api_get_order"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/following/(?P<following_user_id>\d+)%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('following_detail'), name="api_following_detail"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/following%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_following'), name="api_get_following"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/followers%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_followers'), name="api_get_followers"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/comments%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_received_comments'), name="api_get_received_comments"),
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
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/users_nearby%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_users_nearby'), name="api_get_users_nearby"),   
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/photos%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('view_upload_photos'), name="api_view_upload_photos"),   
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/location%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('update_location'), name="api_update_location"),   
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/avatar%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('avatar'), name="api_avatar"),  
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/visitors%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('visit'), name="api_visit"),            
        ]
    
    def obj_update(self, bundle, request=None, **kwargs):
        """
        A quick and dirty fix as tastypie seems to have problems with even simple PATCH request.
        By overwritting this method, PUT request may not work, and any PATCH request that tries to update foreign keys or m2m relations will not work either.
        Hope this will be a new version of tastypie, or we shall use a complete new rest framework.  
        """
#        nameChanged = False
#        if bundle.data['name'] != bundle.obj.name:
#            nameChanged = True
        bundle = self.full_hydrate(bundle)
        self.save_related(bundle)
        if bundle.data['email']:
            bundle.obj.user.email = bundle.data['email']
            bundle.obj.user.save()
        bundle.obj.save()
        # if nameChanged:
        #     logger.debug('sync name to xmpp server')
        #     xmpp_client.syncProfile(bundle.obj )
        return bundle
    
    def get_order(self, request, **kwargs):
        if not request.user.is_authenticated():
            return login_required(request)
        user_profile = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        order_resource = OrderResource()

        if request.method == 'POST':
            meal = Meal.objects.get(id=request.POST.get('meal_id'))
            num_persons = int(request.POST.get('num_persons'))
            #TODO try catch if no avaliable seats
            try:
                order = meal.join(user_profile, num_persons)
                order_resource = OrderResource()
                order_bundle = order_resource.build_bundle(obj=order)
                serialized = order_resource.serialize(None, order_resource.full_dehydrate(order_bundle),  'application/json')
                dic = json.loads(serialized)
                app_req_str = create_app_pay(order.id, order.meal.topic, meal.list_price * num_persons)
                dic['app_req_str'] = app_req_str
                return createGeneralResponse('OK', "You've just joined the meal",dic)
            except NoAvailableSeatsError, e:
                return createGeneralResponse('NOK', e.message)
        else:
            obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
            all_valid_orders = obj.get_paying_orders() | obj.get_upcomming_orders() | obj.get_passedd_orders()
            return self.get_my_list(OrderResource(), all_valid_orders, request)# order_resource.get_list(request, customer=user_profile)
    
    def get_following(self, request, **kwargs):
        if not request.user.is_authenticated():
            return login_required(request)
        
        me = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))        
        if request.method == 'POST':
            user_to_be_followed = UserProfile.objects.get(id=request.POST.get('user_id'))
            relationship = Relationship(from_person=me, to_person=user_to_be_followed)
            relationship.save()
            return createGeneralResponse('OK', 'You are now following %s' % user_to_be_followed)
        else:
            obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
            return self.get_my_list(self, obj.following.all(), request) 
    
    def following_detail(self, request, **kwargs):
        if not request.user.is_authenticated():
            return login_required(request)
        to_person_id = kwargs['following_user_id']
        del(kwargs['following_user_id'])
        me = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))        
        if request.method == 'DELETE':
            user_to_be_not_followed = UserProfile.objects.get(id=to_person_id)
            relationship = Relationship.objects.get(from_person=me, to_person=user_to_be_not_followed) 
            relationship.delete()
            return createGeneralResponse('OK', 'You are not following %s anymore' % user_to_be_not_followed)
        else:
            raise
        
    def get_followers(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        return self.get_my_list(self, obj.followers.all(), request) 
    
    def get_recommended_following(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        return self.get_my_list(self, obj.recommended_following.all(), request) 
    
    def get_received_comments(self, request, **kwargs):
        if not request.user.is_authenticated():
            return login_required(request)
        
        if request.method == 'GET':
            user_to_query = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs)) 
            return self.get_my_list(UserMessageResource(), user_to_query.received_comments, request)
        else:
            raise NotImplementedError
                
    def get_invitation(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        return self.get_my_list(MealInvitationResource(), obj.invitations, request)
    
    def get_meal(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        return self.get_my_list(MealResource(), obj.meals, request)
    
    def get_tags(self, request, **kwargs):
        if not request.user.is_authenticated():
            return login_required(request)
        
        user = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))        
        if request.method == 'POST':
            if request.POST.get('tags'):
                tags = [token.strip() for token in request.POST.get('tags').split(' ')]
                user.tags.set(*tags)
                return createGeneralResponse('OK', 'tags %s set' % tags)
            elif request.POST.get('tag'):
                user.tags.add(request.POST.get('tag'))
                return createGeneralResponse('OK', 'tag %s added' % request.POST.get('tag'))
            else:
                raise
        else:
            return self.get_my_list(UserTagResource(), user.tags.all(), request) 

    # we need to do the filtering of list by ourselves as tastypie filters only queryset
    def filter_list(self, request, users):
        if request.GET.get('gender'):
            gender = int(request.GET.get('gender'))
            users = [u for u in users if u.gender == gender]
        if request.GET.get('seen_within_minutes'):
            minutes = int(request.GET.get('seen_within_minutes'))
            users = [u for u in users if datetime.now() - u.faked_location.updated_at < timedelta(minutes=minutes)]    
        return users
        
    def get_recommendations(self, request, **kwargs):
        if not request.user.is_authenticated():
            return login_required(request)
        if request.method == 'GET':
            user_to_query = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))   
            recommendations = user_to_query.recommendations    
            return self.get_my_list(UserResource(), self.filter_list(request, recommendations), request)
        else:
            raise
    
    def get_users_nearby(self, request, **kwargs):
        if not request.user.is_authenticated():
            return login_required(request)
        if request.method == 'GET':
            user_to_query = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs)) 
            lat = request.GET.get("lat")
            lng = request.GET.get("lng")
            if lat and lng:
                users = user_to_query.users_nearby(lat, lng)
            else:
                users = user_to_query.users_nearby()
            return self.get_my_list(UserResource(), self.filter_list(request, users), request)
        else:
            raise
    
    def view_upload_photos(self, request, **kwargs):
        user_to_query = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))   
        if request.method == 'GET':
            photos = user_to_query.photos.all()
            return self.get_my_list(UserPhotoResource(), photos, request)
        elif request.method == "POST":
            photo = UserPhoto(user=user_to_query)
            name = request.FILES.keys()[0]
            photo.photo.save(name, request.FILES.values()[0])
            photo_resource = UserPhotoResource()
            photo_bundle = photo_resource.build_bundle(obj=photo)
            serialized = photo_resource.serialize(None, photo_resource.full_dehydrate(photo_bundle),  'application/json')
            dic = json.loads(serialized)
            return createGeneralResponse('OK', 'Photo uploaded.' , dic)
        elif request.method == 'DELETE':
            raise NotImplementedError        
    
    def update_location(self, request, **kwargs):
        user_to_query = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))   
        if request.method == "POST":
            location = None
            if user_to_query.location:
                location = user_to_query.location
            else:
                location = UserLocation()
            location.lat = request.POST.get("lat")
            location.lng = request.POST.get("lng")
            location.updated_at = datetime.now()
            location.save()
            user_to_query.location = location
            user_to_query.save()
            return createGeneralResponse('OK', 'Photo uploaded.') # , {"id":photo.id, "photo":photo.photo}
        elif request.method == 'DELETE':
            raise NotImplementedError
        
    def visit(self, request, **kwargs):
        host = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))   
        if request.method == "POST":
            visitor = UserProfile.objects.get(id=request.POST.get('visitor_id'))
            Visitor.objects.get_or_create(from_person=visitor, to_person=host)
            return createGeneralResponse('OK', 'You visited %s' % host)
        else:
            raise NotImplementedError 
    
    def avatar(self, request, **kwargs):
        user_to_query = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))   
        if request.method == "GET":
            width = request.GET.get("width")
            height = request.GET.get("height")
            if not width or not height:
                return createGeneralResponse('NOK', 'width and height expected') 
            url = user_to_query.avatar_thumbnail(int(width), int(height))
            return createGeneralResponse('OK', 'user thumbnail ok', {"url": url})
        elif request.method == 'POST':
            if user_to_query.avatar:
                old_avatar_path = user_to_query.avatar.path
            else:
                old_avatar_path = None
            contentFile = request.FILES.values()[0]
            filename = contentFile.name
            user_to_query.cropping = "" #cropping is not supported by app yet so clear it
            user_to_query.avatar.save(filename, contentFile)
            if os.path.exists(old_avatar_path) and user_to_query.avatar.path != old_avatar_path:
                os.remove(old_avatar_path)
            # xmpp_client.syncProfile(user_to_query)
            user_resource = UserResource()
            ur_bundle = user_resource.build_bundle(obj=user_to_query)
            serialized = user_resource.serialize(None, user_resource.full_dehydrate(ur_bundle),  'application/json')
            dic = json.loads(serialized)
            return createGeneralResponse('OK', 'avatar uploaded.' , dic)
        elif request.method == 'DELETE':
            raise NotImplementedError
               
    class Meta:
        authorization = Authorization()
        queryset = UserProfile.objects.all()
        resource_name = 'user'
        filtering = {'from_user':ALL,'gender': ALL, 'user': ALL_WITH_RELATIONS, "id":ALL}
        allowed_methods = ['get', 'post', 'put', 'patch']


class RelationshipResource(EOResource):
    from_person = fields.ForeignKey(UserProfile, 'from_person')
    to_person = fields.ForeignKey(UserProfile, 'to_person')
    
    class Meta:
        queryset = Relationship.objects.all()
        filtering = {'from_person': ALL_WITH_RELATIONS,
                     'to_person': ALL_WITH_RELATIONS,}

#TODO what if pagination is needed for comments?
class RestaurantResource(EOResource):
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/rating%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_rating'), name="api_get_rating"),
        ]
    
    
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
        filtering = {
            'name': ALL,         
            'tel': ALL,
            'longitude': ALL,
            'latitude': ALL,
            'tags': ALL_WITH_RELATIONS,
            'regions': ALL_WITH_RELATIONS,
            'user_favorite': ALL_WITH_RELATIONS,
        }

     
class UserMessageResource(EOResource): 
    from_person = fields.ForeignKey(UserResource, 'from_person', full=True)
    to_person = fields.ForeignKey(UserResource, 'to_person', full=True )
    
    class Meta:
        queryset = UserMessage.objects.all()
        filtering = {'from_person': ALL_WITH_RELATIONS,
                     'to_person': ALL_WITH_RELATIONS,
                     'type':ALL,}

class DishCategoryResource(EOResource):
    class Meta:
        queryset = DishCategory.objects.all()       


class DishCategoryItemResource(EOResource):
    category = fields.ToOneField(DishCategoryResource, 'category', full=True)
    class Meta:
        queryset = DishCategoryItem.objects.all()
        
class MenuResource(EOResource):
    dishcategoryitem_set = fields.ToManyField(DishCategoryItemResource, 'dishcategoryitem_set', full=True)
    class Meta:
        queryset = Menu.objects.all()
    
class MealResource(EOResource):
    restaurant = fields.ForeignKey(RestaurantResource, 'restaurant', full=True)
    host = fields.ForeignKey(SimpleUserResource, 'host', full=True)
    participants = fields.ToManyField(MealParticipantResource, 'mealparticipants_set', full=True, null=True)
    
    def hydrate(self, bundle):
        bundle.data['actual_persons']=1
        if not bundle.data.get('max_persons'):
            bundle.data['max_persons'] = bundle.data['min_persons']
        
    def dehydrate(self, bundle):
        bundle.data["photo"] = bundle.obj.big_cover_url
        return bundle
        
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/comments%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_comments'), name="api_get_comments"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/menu%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_menu'), name="api_get_menu"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/likes%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('like'), name="api_like"),
        ]
    
    def get_menu(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        menu_resource = MenuResource()
        return self.get_my_list(menu_resource, [obj.menu], request)
                           
    def get_comments(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        meal_comment_resource = MealCommentResource()
        return self.get_my_list(meal_comment_resource, obj.comments.all(), request)
           
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
        filtering = {'type': ALL,'start_date':ALL, "id":ALL}
        allowed_methods = ['get','post']
        authorization = Authorization()
        ordering = ['start_date']

class MealCommentResource(EOResource):
    from_person = fields.ForeignKey(UserResource, 'from_person', full=True)
    meal  = fields.ForeignKey(MealResource, 'meal')
    
    class Meta:
        queryset = MealComment.objects.all()
        filtering= {'meal': ALL}
    
class MealInvitationResource(EOResource):
    from_person = fields.ForeignKey(UserResource, 'from_person', full=True)
    to_person = fields.ForeignKey(UserResource, 'to_person', full=True)
    meal = fields.ForeignKey(MealResource, 'meal', full=True)
    
    class Meta:
        queryset = MealInvitation.objects.all()
        filtering = {'from_person':ALL_WITH_RELATIONS, 
                     'to_person': ALL_WITH_RELATIONS,
                     }
        resource_name = 'invitation'

class OrderResource(EOResource):        
    meal = fields.ForeignKey(MealResource,'meal', full=True)
    customer = fields.ToOneField(UserResource, 'customer', full=True)
        
    class Meta:
        queryset = Order.objects.all() # .exclude(status=4)
        filtering = {'customer':ALL_WITH_RELATIONS, 'meal':ALL_WITH_RELATIONS, "status":ALL}
        ordering = ['created_time','meal']
            
def createLoggedInResponse(loggedInuser):
    user_resource = UserResource()
    ur_bundle = user_resource.build_bundle(obj=loggedInuser.get_profile())
    serialized = user_resource.serialize(None, user_resource.full_dehydrate(ur_bundle),  'application/json')
    dic = json.loads(serialized)
    dic['status'] = 'OK'
    dic['info'] = "You've logged in"
    return HttpResponse(json.dumps(dic), content_type ='application/json')
            
def mobile_user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = None
        try:
            user = User.objects.create_user(username, '', password)
            p = re.compile(".+@.+\..+")
            if p.match(username):
                user.email = username
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return createLoggedInResponse(user)
        except IntegrityError:
            if user:
                user.delete()
            return createGeneralResponse('NOK', "That username already exists")
    else:
        raise # not used by mobile client     

def checkemail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        usersWithEmail = User.objects.filter(email=email)
        if len(usersWithEmail) > 0:
            return createGeneralResponse("NOK", "That email already exists")
        else:
            return createGeneralResponse("OK", "email is OK to use")
    else:
        raise
    
def weibo_user_login(request):
    if request.method == 'POST':        
        # logs the user in as he has been authenticated by weibo at the mobile client side already. 
        # a new uesr might be created if this is the first time the user logs in, check WeiboAuthenticationBackend
        post_dict = dict(request.POST.items()) # POST.dict() is available since django 1.4
        user_to_authenticate = auth.authenticate(**post_dict)
        if user_to_authenticate:
            auth.login(request, user_to_authenticate)
            return createLoggedInResponse(user_to_authenticate)
        else:
            return createGeneralResponse('NOK', "Login failed")
    else:
        raise # not used by mobile client   
       
def mobile_user_login(request):
    if request.method == 'POST':
#        return createGeneralResponse('NOK', "Currently only logging in from sina weibo is possible")
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
#            user_resource = UserResource()
#            ur_bundle = user_resource.build_bundle(obj=user.get_profile())
#            serialized = user_resource.serialize(None, user_resource.full_dehydrate(ur_bundle),  'application/json')
#            dic = json.loads(serialized)
##            dic = {}
#            dic['status'] = 'OK'
#            dic['info'] = "You've logged in"
#            return HttpResponse(json.dumps(dic), content_type ='application/json')
            return createLoggedInResponse(user)
        else:
            return createGeneralResponse('NOK', "Incorrect username or password")
    else:
        raise # not used by mobile client
    
def mobile_user_logout(request):
    if request.method == 'POST':
        profile = request.user.get_profile()
        profile.apns_token = ""
        profile.save()
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
v1_api.register(DishCategoryResource())
v1_api.register(OrderResource())
v1_api.register(RelationshipResource())
v1_api.register(MealResource())
v1_api.register(MealInvitationResource())
v1_api.register(UserLocationResource())
v1_api.register(MealCommentResource())
v1_api.register(UserTagResource())
v1_api.register(UserPhotoResource())
v1_api.register(SimpleUserResource())