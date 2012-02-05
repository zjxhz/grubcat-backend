from django.conf.urls.defaults import *
from grubcat.eo.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       ('^hello/$', hello),
                       ('^get_menu/$',get_menu),
                       ('^get_restaurant_list_by_geo/$',get_restaurant_list_by_geo),
                       ('^search_restaurant_list/$',restaurantList),
                       ('^user_login/$',user_login),
                       ('^login/$',login),
                       ('^test_make_order/$',test_make_order),
                       ('^make_order/$',make_order),
                       ('^order/$',get_orders),
                       ('^order/(\d+)/$',get_order_by_id),
                       ('^profile/$',get_user_profile),
                       ('^profile/favorite/restaurant/(\d+)/$',favorite_restaurant),
                       ('^profile/favorite/restaurant/$',favorite_restaurants),
    # Example:
    # (r'^grubcat/', include('grubcat.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
