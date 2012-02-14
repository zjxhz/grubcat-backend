from django.conf.urls.defaults import *
from grubcat.eo.views import *
from grubcat.eo.db import updateLatLng

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       ('^hello/$', hello),
                       ('^get_menu/$',get_menu),
                       ('^get_restaurant_list_by_geo/$',get_restaurant_list_by_geo),
                       ('^restaurant/(\d+)/$', get_restaurant),
                       ('^restaurant/(\d+)/dish/recommendation/$', get_recommended_dishes),
                       ('^restaurant/(\d+)/comments/$', restaurant_comments),
                       ('^restaurant_tag/$', get_restaurant_tags),
                       ('^restaurant_tag/(\d+)/restaurant/$', get_restaurants_with_tag),
                       ('^business_district/$', get_business_districts),
                       ('^business_district/(\d+)/restaurant/$', get_restaurants_in_business_district),
                       ('^search_restaurant_list/$',restaurantList),
                       ('^user_login/$',user_login),
                       ('^user_logout/$',user_logout),
                       ('^login/$',login),
                       ('^logout/$',logout),
                       ('^test_make_order/$',test_make_order),
                       ('^make_order/$',make_order),
                       ('^order/$',get_orders),
                       ('^order/(\d+)/$',get_order_by_id),
                       ('^profile/$',get_user_profile),
                       ('^profile/favorite/restaurant/(\d+)/$',favorite_restaurant),
                       ('^profile/favorite/restaurant/$',favorite_restaurants),
                       ('^register/$',register),

                       # developer interfaces...
                       ('^updateLatLng/$', updateLatLng),
    # Example:
    # (r'^grubcat/', include('grubcat.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
