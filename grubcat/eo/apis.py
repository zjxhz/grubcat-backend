from tastypie.resources import ModelResource
from eo.models import *
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.paginator import Paginator
import copy
from urllib import urlencode
from tastypie.api import Api
from django.conf.urls.defaults import url
from tastypie.utils import trailing_slash
from tastypie.constants import ALL, ALL_WITH_RELATIONS

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
        
        
class UserResource(ModelResource):
    user = fields.ForeignKey(DjangoUserResource, 'user', full=True)

    def dehydrate(self, bundle):
        for key in bundle.data['user'].data:
            bundle.data[key] = bundle.data['user'].data[key]
        del bundle.data['user']
        return bundle
        
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'user'
        

class RestaurantResource(ModelResource):
    class Meta:
        queryset = Restaurant.objects.all()
        paginator_class = PageNumberPaginator
        filtering = {
            'tel': ALL,
            'tags': ALL_WITH_RELATIONS,
        }

class RestaurantsWithTagResource(ModelResource):
    class Meta:
        queryset = Restaurant.objects.all()
        paginator_class = PageNumberPaginator        
        
class RestaurantTagResource(ModelResource):
    #restaurant = fields.ToManyField(RestaurantResource, 'restaurant')
    #restaurants = fields.ToManyField('eo.apis.RestaurantResource', 'restaurant_set', related_name='restaurant')
    #restaurants = fields.ToManyField(RestaurantResource, 'restaurant')

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/restaurant%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_restaurants'), name="api_get_restaurants"),
        ]
    
    def get_restaurants(self, request, **kwargs):
        obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        restaurant_resource = RestaurantResource()
        tag = RestaurantTag.objects.get(id=obj.pk)
        print obj, obj.pk, tag
        return restaurant_resource.get_list(request, tags=tag)
        #return restaurant_resource.get_detail(request, tags=tag)
        #return restaurant_resource.get_list(request, tel__startswith='0571')
    
    class Meta:
        queryset = RestaurantTag.objects.all()
        resource_name = 'restaurant_tag'


        
v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(DjangoUserResource())
v1_api.register(RestaurantResource())
v1_api.register(RestaurantTagResource())
