from django.conf.urls.defaults import *
from grubcat.eo.views import *
from grubcat import settings
from grubcat.eo.db import *

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
                       ('^test_make_order/$',test_make_order),
                       ('^make_order/$',make_order),
                       ('^order/$',get_orders),
                       ('^order/(\d+)/$',get_order_by_id),
                       ('^profile/$',get_user_profile),
                       ('^profile/favorite/restaurant/(\d+)/$',favorite_restaurant),
                       ('^profile/favorite/restaurant/$',favorite_restaurants),
                       ('^register/$',register),
                       ('^restaurant/new/$',add_restaurant),
                       ('^search/restaurant/$', query_restaurant_from_google),
                       
                        #social
                       ('^user/(\d)/$', get_user_profile),
                       ('^user/(\d)/following/$', get_following),
                       ('^user/(\d)/following/remove/$', remove_following),
                       ('^user/(\d)/followers/$', followers),
                       ('^user/(\d)/following/recommendations/$', get_recommended_following),
                       ('^user/(\d)/messages/$',messages),
                       ('^meal/$',get_meals),
                       ('^meal/(\d)/$',get_meal),
                       ('^meal/(\d)/participants/$',meal_participants),
                       
                       # developer interfaces...
                       ('^updateLatLng/$', updateLatLng),
                       ('^img_test/$',img_test),
                       ('^upload_file/$',upload_file),
                       

                       # HTML
                       ('^restaurant/(\d+)/dish/add/$',add_dish),
    # Example:
    # (r'^grubcat/', include('grubcat.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,}),)
    urlpatterns += staticfiles_urlpatterns()
