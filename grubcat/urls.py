import django
from django.conf.urls.defaults import *
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from eo.apis import v1_api
from eo.db import query_restaurant_from_google, updateLatLng
from eo.views import hello, get_menu, get_restaurant_list_by_geo, get_restaurant,\
    get_recommended_dishes, restaurant_rating, get_restaurant_tags,\
    get_restaurants_with_tag, get_regions, get_restaurants_in_region, restaurantList,\
    user_login, user_logout, test_make_order, make_order, get_orders,\
    get_order_by_id, get_user_profile, favorite_restaurant, favorite_restaurants,\
    add_restaurant, get_following, remove_following, followers,\
    get_recommended_following, register, messages, get_meals, get_meal,\
    meal_participants, view_or_send_meal_invitations,\
    accept_or_reject_meal_invitations, img_test, upload_app, add_dish
from grubcat.eo.db import *
from grubcat.eo.views import *
import settings

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    ('^hello/$', hello),
    ('^get_menu/$', get_menu),
    ('^get_restaurant_list_by_geo/$', get_restaurant_list_by_geo),
    ('^restaurant/(\d+)/$', get_restaurant),
    ('^restaurant/(\d+)/dish/recommendation/$', get_recommended_dishes),
    ('^restaurant/(\d+)/rating/$', restaurant_rating),
    ('^restaurant_tag/$', get_restaurant_tags),
    ('^restaurant_tag/(\d+)/restaurant/$', get_restaurants_with_tag),
    ('^region/$', get_regions),
    ('^region/(\d+)/restaurant/$', get_restaurants_in_region),
    ('^search_restaurant_list/$', restaurantList),
    ('^user_login/$', user_login),
    ('^user_logout/$', user_logout),
    ('^test_make_order/$', test_make_order),
    ('^make_order/$', make_order),
    ('^order/$', get_orders),
    ('^order/(\d+)/$', get_order_by_id),
    ('^profile/$', get_user_profile),
    ('^profile/favorite/restaurant/(\d+)/$', favorite_restaurant),
    ('^profile/favorite/restaurant/$', favorite_restaurants),
    ('^register/$', register),
    ('^restaurant/new/$', add_restaurant),
    ('^search/restaurant/$', query_restaurant_from_google),

    #social
    ('^user/(\d+)/$', get_user_profile),
    ('^user/(\d+)/following/$', get_following),
    ('^user/(\d+)/following/remove/$', remove_following),
    ('^user/(\d+)/followers/$', followers),
    ('^user/(\d+)/following/recommendations/$', get_recommended_following),
    ('^user/(\d+)/messages/$', messages),
    ('^meal/$', get_meals),
    #   ('^meal/(\d+)/$', get_meal),
    ('^meal/(\d+)/participants/$', meal_participants),
    ('^user/(\d+)/invitation/$', view_or_send_meal_invitations),
    ('^user/(\d+)/invitation/(\d+)/$', accept_or_reject_meal_invitations),

    # developer interfaces...
    ('^updateLatLng/$', updateLatLng),
    ('^img_test/$', img_test),
    ('^upload_app/$', upload_app),

    # HTML
    (r'^$', MealListView.as_view()),
    ('^restaurant/(\d+)/dish/add/$', add_dish),
    (r'^meals/$', MealListView.as_view()),
    url(r'^meal/(?P<pk>\d+)/$', DetailView.as_view(
        model=Meal, context_object_name="meal", template_name="meal/meal_detail.html"), name='meal_view'),
    # Example:
    # (r'^grubcat/', include('grubcat.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    #server media files and static files in developement environment
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

# Standard bits...
urlpatterns += patterns('',
    (r'^api/', include(v1_api.urls)),
)
