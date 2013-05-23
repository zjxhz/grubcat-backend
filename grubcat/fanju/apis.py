#coding=utf-8
from api_auth import UserObjectsOnlyAuthorization
from datetime import datetime, timedelta
from django.conf.urls.defaults import url
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import logout
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseForbidden
from exceptions import NoAvailableSeatsError
from models import UserLocation, UserTag, UserPhoto, User, MealParticipants, \
    Meal, Relationship, UserMessage, Visitor, Restaurant, DishCategory, \
    DishCategoryItem, MealComment, Order, Menu, Dish, DishItem
from pay.alipay.alipay import create_app_pay
from taggit.models import Tag
from tastypie import fields, http
from tastypie.api import Api
from tastypie.authorization import Authorization, ReadOnlyAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.fields import RelatedField
from tastypie.http import HttpUnauthorized
from tastypie.paginator import Paginator
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from tastypie.utils.dict import dict_strip_unicode_keys
from urllib import urlencode
import json
import logging
import os
import re

logger = logging.getLogger(__name__)

# page starts from 1
class PageNumberPaginator(Paginator):
    def page(self):
        output = super(PageNumberPaginator, self).page()
        meta = output['meta']
        meta['page_number'] = self.get_page()
        if self.get_count() % self.get_limit() == 0:
            meta['tatal_pages'] = self.get_count() / self.get_limit()
        else:
            meta['tatal_pages'] = self.get_count() / self.get_limit() + 1
        del meta['offset']
        
        return output
               
    def get_offset(self):
        self.offset = self.get_limit() * (self.get_page() - 1)
        return self.offset 
    
    def get_page(self):
        page = self.request_data.get('page')
        if page:
            return int(page)
        return 1    

class EOResource(ModelResource):
    def __init__(self):
        super(EOResource, self).__init__()
        self._meta.paginator_class = PageNumberPaginator
        
        
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
        sorted_objects = resource.apply_sorting(queryset, options=request.GET)
    
        paginator = resource._meta.paginator_class(request.GET, sorted_objects, 
                                                   resource_uri=resource.get_resource_uri(),
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

    
    def obj(self, request, **kwargs):
        basic_bundle = self.build_bundle(request=request)
        return self.cached_obj_get(basic_bundle, **self.remove_api_resource_names(kwargs))
        
# compatible with 0.9.11, RelatedField.should_full_dehydrate now checks request which is not always available, let's make it return True as long as "full" presents
#def should_full_dehydrate(relatedField, bundle):
#    return relatedField.full
#RelatedField.should_full_dehydrate = should_full_dehydrate

#todo maybe we can use decorator
def login_required(request):
    response = {"status": "NOK", "info": "You were not logged in"}
    return HttpUnauthorized(json.dumps(response))
         
class SuccessResponse(HttpResponse):
    def __init__(self, extra_dict=None):
        content = {"status": "OK", "info":"ALL is well"}
        if extra_dict:
            content.update(extra_dict)
        content = json.dumps(content)
        super(SuccessResponse, self).__init__(content = content, content_type="application/json")
    
#class DjangoUserResource(EOResource):
#    class Meta:
#        queryset = User.objects.all()
#        resource_name = 'django_user'
#        fields = ['username', 'email', 'date_joined']
#        allowed_methods = ['get']
#        filtering = {'username': ALL, 'email':ALL}

class UserLocationResource(EOResource):
    class Meta:
        allowed_methods = ['get']
        queryset = UserLocation.objects.all()
        authorization = UserObjectsOnlyAuthorization(True)

class UserTagResource(EOResource):
    def prepend_urls(self):
        return [url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/users%s$" % (self._meta.resource_name, trailing_slash()),
            self.wrap_view('users'), name="api_users"),]
    
    def users(self, request, **kwargs):
        user_tag = self.obj(request, **kwargs)
        if request.method == 'GET':
            return self.get_my_list(UserResource(), user_tag.tagged_users(), request )                    
    class Meta:
        allowed_methods = ['get']
        authorization = ReadOnlyAuthorization() # can be updated at /user/u_id/tags/
        queryset = UserTag.objects.all()

class UserPhotoResource(EOResource):
    def post_list(self, request, **kwargs):
        # in a REST framework there is no easy way to delete multiple objects at a time, so just use post here
        deleted_ids = request.POST.get("deleted_ids")
        if deleted_ids:
            for deleted_id in deleted_ids.split(","):
                photo = UserPhoto.objects.get(pk=deleted_id)
                if photo.user == request.user:
                    photo.delete()
                else:
                    return HttpResponseForbidden()
            return SuccessResponse()  
        else:
            return super(UserPhotoResource, self).post_list(request, **kwargs)
                          
    def dehydrate(self, bundle):
        bundle.data['thumbnail'] = bundle.obj.photo_thumbnail
        bundle.data['large'] = bundle.obj.large_photo
        return bundle
    
    class Meta:
        queryset = UserPhoto.objects.all()
        authorization = UserObjectsOnlyAuthorization(read_other=True)
        filtering={"id":ALL}
        allowed_methods = ['get', 'post', 'delete']


def dehydrate_basic_userinfo(resource, bundle):
    if not bundle.data['location']:
        # simulate a location. TODO remove these lines in production
        bundle.data['lat'] = 30.275
        bundle.data['lng'] = 120.148
        bundle.data['updated_at'] = "2012-10-16"
    bundle.data['small_avatar'] = bundle.obj.normal_avatar #small is too small for iPhone
    bundle.data['big_avatar'] = bundle.obj.big_avatar
    resource.mergeOneToOneField(bundle, 'location', ['id', ])
    
#    request_user = bundle.request.user
#    if request_user and request_user.is_authenticated() and request_user.is_following(bundle.obj):
#        bundle.data["following"] = True
#    else:
#        bundle.data["following"] = False
    return bundle

class SimpleUserResource(EOResource):
    location = fields.ToOneField(UserLocationResource, 'location', full=True, null=True)
    def dehydrate(self, bundle):
        return dehydrate_basic_userinfo(self, bundle)
    
    class Meta:
        queryset = User.objects.all()
        authorization = UserObjectsOnlyAuthorization(True)
        excludes=['password','weibo_access_token']
        resource_name = 'simple_user'
        filtering = {'id':ALL, 'username':ALL, 'name':ALL}

class MealParticipantResource(EOResource):
    user = fields.ForeignKey(SimpleUserResource, 'user', full=True)
    
    def dehydrate(self, bundle):
        self.mergeOneToOneField(bundle, 'user')
        return bundle

    class Meta:
        queryset = MealParticipants.objects.all()
        authorization = ReadOnlyAuthorization()

            
def readMineOnly(func):
    """
    decorator that allows user to read records that belong to her/himself only
    """
    def inner(self, request, **kwargs):
        if not request.user.is_authenticated():
            return http.HttpUnauthorized()
        resource_profile = self.obj(request, **kwargs)
        request_profile = request.user
        if resource_profile == request_profile:
            return func(self, request, **kwargs)
        else:
            return http.HttpUnauthorized()
    return inner
            
def writeMineOnly(func):
    """
    decorator that allows user to write records that belong to her/himself only, but the user is allowed to read other's records like followers
    """
    def inner(self, request, **kwargs):
        if not request.user.is_authenticated():
            return http.HttpUnauthorized()
        resource_profile = self.obj(request, **kwargs)
        request_profile = request.user
        if not request.method == "GET" and resource_profile != request_profile:
            return http.HttpUnauthorized()
        else:
            return func(self, request, **kwargs)
    return inner
            
class UserResource(EOResource):
    location = fields.ToOneField(UserLocationResource, 'location', full=True, null=True)
    tags = fields.ToManyField(UserTagResource, 'tags', full=True, null=True)
    photos = fields.ToManyField(UserPhotoResource, 'photos', full=True, null=True)

    def hydrate(self, bundle):
        bundle.data['avatar'] = str(bundle.obj.avatar) # never change avatar in a patch request, or it always add /media/
        return bundle
        
    def dehydrate(self, bundle):
        return dehydrate_basic_userinfo(self, bundle)
       
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/order%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('view_order'), name="api_view_order"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/following/(?P<following_user_id>\d+)%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('following_detail'), name="api_following_detail"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/following%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('view_following'), name="api_view_following"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/followers%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('view_followers'), name="api_view_followers"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/comments%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_received_comments'), name="api_get_received_comments"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/meal%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_meal'), name="api_get_meal"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/feeds%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_feeds'), name="api_get_feeds"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/tags%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('view_tags'), name="api_view_tags"),    
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
        """
#        nameChanged = False
#        if bundle.data['name'] != bundle.obj.name:
#            nameChanged = True
        request_profile = request.user
        updated_profile = self.obj(request,**kwargs)
        if not request_profile == updated_profile:
            return http.HttpUnauthorized()
        bundle = self.full_hydrate(bundle)
        self.save_related(bundle)
        if 'email' in bundle.data:
            bundle.obj.email = bundle.data['email']
            bundle.obj.save()
        bundle.obj.save()
        # if nameChanged:
        #     logger.debug('sync name to xmpp server')
        #     xmpp_client.syncProfile(bundle.obj )
        return bundle
    
    @readMineOnly
    def view_order(self, request, **kwargs):
        user_profile = self.obj(request, **kwargs)
        order_resource = OrderResource()

        if request.method == 'POST':
            meal = Meal.objects.get(id=request.POST.get('meal_id'))
            num_persons = int(request.POST.get('num_persons'))
            try:
                order = meal.join(user_profile, num_persons)
                order_resource = OrderResource()
                order_bundle = order_resource.build_bundle(obj=order)
                serialized = order_resource.serialize(None, order_resource.full_dehydrate(order_bundle),  'application/json')
                dic = json.loads(serialized)
                app_req_str = create_app_pay(order.id, order.meal.topic, meal.list_price * num_persons)
                dic['app_req_str'] = app_req_str
                return SuccessResponse(dic)
            except NoAvailableSeatsError, e:
                logger.warn("no available seat when joining %s", e)
                return http.HttpApplicationError()
            except Exception, e:
                logger.error("failed to create an order: ", e)
                return http.HttpApplicationError(e.message)
        else:
            obj = self.obj(request, **kwargs)
            all_valid_orders = obj.get_paying_orders() | obj.get_upcomming_orders() | obj.get_passed_orders()
            return self.get_my_list(OrderResource(), all_valid_orders, request)# order_resource.get_list(request, customer=user_profile)
    
    @writeMineOnly
    def view_following(self, request, **kwargs):        
        me = self.obj(request, **kwargs)        
        if request.method == 'POST':
            user_to_be_followed = User.objects.get(id=request.POST.get('user_id'))
            Relationship.objects.get_or_create(from_person=me, to_person=user_to_be_followed)
            return SuccessResponse()
        else:
            obj = self.obj(request, **kwargs)
            return self.get_my_list(self, obj.following.all(), request) 
    
    @writeMineOnly
    def following_detail(self, request, **kwargs):
        to_person_id = kwargs['following_user_id']
        del(kwargs['following_user_id'])
        me = self.obj(request, **kwargs)        
        if request.method == 'DELETE':
            user_to_be_not_followed = User.objects.get(id=to_person_id)
            relationship = Relationship.objects.get(from_person=me, to_person=user_to_be_not_followed) 
            relationship.delete()
            return SuccessResponse()
        else:
            return http.HttpBadRequest()
    
    @writeMineOnly    
    def view_followers(self, request, **kwargs):
        if request.method == "GET":
            obj = self.obj(request, **kwargs)
            return self.get_my_list(self, obj.followers.all(), request)
        else:
            return http.HttpBadRequest() 
    
    @writeMineOnly   
    def get_received_comments(self, request, **kwargs):
        if request.method == 'GET':
            user_to_query = self.obj(request, **kwargs) 
            return self.get_my_list(UserMessageResource(), user_to_query.received_comments, request)
        else:
            raise  http.HttpBadRequest() 
    
    @writeMineOnly
    def get_meal(self, request, **kwargs):
        if request.method == "GET":
            obj = self.obj(request, **kwargs)
            return self.get_my_list(MealResource(), obj.upcoming_meals, request)
        else:
            return http.HttpBadRequest()

    @writeMineOnly
    def view_tags(self, request, **kwargs):
        user = self.obj(request, **kwargs)       
        if request.method == 'POST':
            if request.POST.get('tags'):
                tags = [token.strip() for token in request.POST.get('tags').split(' ')]
                user.tags.set(*tags)
                return SuccessResponse()
            elif request.POST.get('tag'):
                user.tags.add(request.POST.get('tag'))
                return SuccessResponse()   
            elif request.POST.get('deleted_tag'):
                user.tags.remove(request.POST.get('deleted_tag'))
                return SuccessResponse()      
            elif request.POST.get('create_tag'):
                t = Tag(name=request.POST.get('create_tag'))
                t.save()
                return SuccessResponse({"id":t.id})   
            else:
                return http.HttpBadRequest()
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
    
    @writeMineOnly    
    def get_recommendations(self, request, **kwargs):
        if request.method == 'GET':
            user_to_query = self.obj(request, **kwargs)   
            recommendations = user_to_query.recommendations    
            return self.get_my_list(UserResource(), self.filter_list(request, recommendations), request)
        else:
            return http.HttpBadRequest()
    
    @writeMineOnly
    def get_users_nearby(self, request, **kwargs):
        if request.method == 'GET':
            user_to_query = self.obj(request, **kwargs) 
            lat = request.GET.get("lat")
            lng = request.GET.get("lng")
            if lat and lng:
                users = user_to_query.users_nearby(lat, lng)
            else:
                users = user_to_query.users_nearby()
            return self.get_my_list(UserResource(), self.filter_list(request, users), request)
        else:
            return http.HttpBadRequest()
   
    @writeMineOnly 
    def view_upload_photos(self, request, **kwargs):
        user_to_query = self.obj(request, **kwargs)   
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
            return SuccessResponse(dic)
        elif request.method == 'DELETE':
            raise http.HttpBadRequest()        
    
    @writeMineOnly
    def update_location(self, request, **kwargs):
        user_to_query = self.obj(request, **kwargs)   
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
            return SuccessResponse()
        else:
            raise http.HttpBadRequest()
    
    def visit(self, request, **kwargs):
        host = self.obj(request, **kwargs)   
        if request.method == "POST":
            visitor = User.objects.get(id=request.POST.get('visitor_id'))
            Visitor.objects.get_or_create(from_person=visitor, to_person=host)
            return SuccessResponse()
        else:
            raise http.HttpBadRequest() 
    
    @writeMineOnly
    def avatar(self, request, **kwargs):
        user_to_query = self.obj(request, **kwargs)   
        if request.method == "GET":
            width = request.GET.get("width")
            height = request.GET.get("height")
            if not width or not height:
                return http.HttpBadRequest()
            url = user_to_query.avatar_thumbnail(int(width), int(height))
            return SuccessResponse({"url": url})
        elif request.method == 'POST':
            if user_to_query.avatar:
                old_avatar_path = user_to_query.avatar.path
            else:
                old_avatar_path = None
            contentFile = request.FILES.values()[0]
            filename = contentFile.name
            user_to_query.cropping = "" #cropping is not supported by app yet so clear it
            user_to_query.avatar.save(filename, contentFile)
            if os.path.exists(
                    old_avatar_path) and user_to_query.avatar.path != old_avatar_path and settings.DEFAULT_FEMALE_AVATAR not in old_avatar_path and settings.DEFAULT_MALE_AVATAR not in old_avatar_path:
                os.remove(old_avatar_path)
            # xmpp_client.syncProfile(user_to_query)
            user_resource = UserResource()
            ur_bundle = user_resource.build_bundle(obj=user_to_query)
            serialized = user_resource.serialize(None, user_resource.full_dehydrate(ur_bundle),  'application/json')
            dic = json.loads(serialized)
            return SuccessResponse(dic)
        else:
            raise http.HttpBadRequest()
               
    class Meta:
        authorization = Authorization()
        queryset = User.objects.all()
        resource_name = 'user'
        filtering = {'from_user':ALL,'gender': ALL, 'user': ALL_WITH_RELATIONS, "id":ALL, "username":ALL}
        allowed_methods = ['get', 'post', 'put', 'patch']
        excludes=['password','weibo_access_token']
        authorization = UserObjectsOnlyAuthorization(True)


class RelationshipResource(EOResource):
    from_person = fields.ForeignKey(SimpleUserResource, 'from_person', full=True) #TODO maybe we don't need "full" for from_person
    to_person = fields.ForeignKey(SimpleUserResource, 'to_person', full=True )
    

    def post_list(self, request, **kwargs):
        if not request.user.is_authenticated():
            return http.HttpUnauthorized()
        from_person = request.user
        to_person_id = request.POST.get("to_person_id")
        to_person = User.objects.get(pk=to_person_id)
        relation, created = Relationship.objects.get_or_create(from_person=from_person, to_person=to_person)
        
        dic = {"id":relation.pk, "created": created}
        return SuccessResponse(dic)
            
    class Meta:
        queryset = Relationship.objects.all()
#        authorization = UserObjectsOnlyAuthorization()
        authorization = Authorization()
        resource_name="relationship"
        filtering = {'from_person':ALL_WITH_RELATIONS,'to_person': ALL_WITH_RELATIONS, 'status': ALL}
        allowed_methods = ['get', 'post', 'put', 'patch', 'delete']
        
#TODO what if pagination is needed for comments?
class RestaurantResource(EOResource):
    class Meta:
        queryset = Restaurant.objects.all()
        authorization = ReadOnlyAuthorization()
     
class UserMessageResource(EOResource): 
    from_person = fields.ForeignKey(UserResource, 'from_person', full=True)
    to_person = fields.ForeignKey(UserResource, 'to_person', full=True )
    
    class Meta:
        queryset = UserMessage.objects.all()
        filtering = {'from_person': ALL_WITH_RELATIONS,
                     'to_person': ALL_WITH_RELATIONS,
                     'type':ALL,}
        authorization = ReadOnlyAuthorization()

class DishCategoryResource(EOResource):
    class Meta:
        queryset = DishCategory.objects.all()  
        authorization = ReadOnlyAuthorization()

class DishResource(ModelResource):
    categories = fields.ToManyField(DishCategoryResource, 'categories', full=True, null=True)
    class Meta:
        queryset = Dish.objects.all()
        
class DishCategoryItemResource(EOResource):
    category = fields.ToOneField(DishCategoryResource, 'category', full=True)
    class Meta:
        queryset = DishCategoryItem.objects.all()
        authorization = ReadOnlyAuthorization()

class DishItemResource(ModelResource):
    dish = fields.ToOneField(DishResource, 'dish', full=True)
    class Meta:
        queryset = DishItem.objects.all()
                
class MenuResource(EOResource):
    dishcategoryitem_set = fields.ToManyField(DishCategoryItemResource, 'dishcategoryitem_set', full=True)
    dishitem_set = fields.ToManyField(DishItemResource, "dishitem_set", full=True)
    class Meta:
        queryset = Menu.objects.all()
        authorization = ReadOnlyAuthorization()
    
class MealResource(EOResource):
    restaurant = fields.ForeignKey(RestaurantResource, 'restaurant', full=True)
    host = fields.ForeignKey(SimpleUserResource, 'host', full=True, null=True)
    participants = fields.ToManyField(MealParticipantResource, 'mealparticipants_set', full=True, null=True)
    
    def hydrate(self, bundle):
        bundle.data['actual_persons']=1
        if not bundle.data.get('max_persons'):
            bundle.data['max_persons'] = bundle.data['min_persons']
        
    def dehydrate(self, bundle):
        bundle.data["photo"] = bundle.obj.big_cover_url
        return bundle
        
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/comments%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_comments'), name="api_get_comments"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/menu%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_menu'), name="api_get_menu"),
            # url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/likes%s$" % (self._meta.resource_name, trailing_slash()),
            #     self.wrap_view('like'), name="api_like"),
        ]
    
    def get_menu(self, request, **kwargs):
        if request.method == "GET":
            obj = self.obj(request, **kwargs)
            menu_resource = MenuResource()
            return self.get_my_list(menu_resource, [obj.menu], request)
        else:
            return http.HttpBadRequest()
                           
    def get_comments(self, request, **kwargs):
        if request.method == "GET":
            obj = self.obj(request, **kwargs)
            meal_comment_resource = MealCommentResource()
            return self.get_my_list(meal_comment_resource, obj.comments.all(), request)
        else:
            return http.HttpBadRequest()
    
    class Meta:
        queryset = Meal.objects.all()
        filtering = {'type': ALL,'start_date':ALL, "id":ALL}
        allowed_methods = ['get','post']
        authorization = ReadOnlyAuthorization()
        ordering = ['start_date']

class MealCommentResource(EOResource):
    from_person = fields.ForeignKey(UserResource, 'from_person', full=True)
    meal  = fields.ForeignKey(MealResource, 'meal')
    
    class Meta:
        queryset = MealComment.objects.all()
        filtering= {'meal': ALL}
        authorization = ReadOnlyAuthorization()
    

class OrderResource(EOResource):        
    meal = fields.ForeignKey(MealResource,'meal', full=True)
    customer = fields.ToOneField(UserResource, 'customer', full=True)
        
    class Meta:
        queryset = Order.objects.all() # .exclude(status=4)
        filtering = {'customer':ALL_WITH_RELATIONS, 'meal':ALL_WITH_RELATIONS, "status":ALL}
        ordering = ['created_time','meal']
        authorization = UserObjectsOnlyAuthorization()
            
def createLoggedInResponse(loggedInuser):
    user_resource = UserResource()
    ur_bundle = user_resource.build_bundle(obj=loggedInuser)
    serialized = user_resource.serialize(None, user_resource.full_dehydrate(ur_bundle),  'application/json')
    dic = json.loads(serialized)
    return SuccessResponse(dic)
            
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
            return http.HttpApplicationError()
    else:
        raise # not used by mobile client     

def checkemail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        usersWithEmail = User.objects.filter(email=email)
        if len(usersWithEmail) > 0:
            return http.HttpApplicationError()
        else:
            return SuccessResponse()
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
            return http.HttpUnauthorized()
    else:
        raise # not used by mobile client   
       
def mobile_user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return createLoggedInResponse(user)
        else:
            return http.HttpUnauthorized()
    else:
        raise # not used by mobile client
    
def mobile_user_logout(request):
    if request.method == 'POST':
        profile = request.user
        if profile.is_authenticated():
            profile.apns_token = ""
            profile.save()
            logout(request)
        return SuccessResponse()
    else:
        return http.HttpBadRequest() 
    
v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(RestaurantResource())
v1_api.register(DishCategoryResource())
v1_api.register(OrderResource())
v1_api.register(MealResource())
v1_api.register(UserLocationResource())
v1_api.register(MealCommentResource())
v1_api.register(UserTagResource())
v1_api.register(UserPhotoResource())
v1_api.register(SimpleUserResource())
v1_api.register(RelationshipResource())