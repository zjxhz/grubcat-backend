import django
from django.conf.urls.defaults import *
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from eo.apis import v1_api, mobile_user_login, mobile_user_logout
from eo.db import query_restaurant_from_google, updateLatLng
from eo.decorators import restaurant_login_required
from eo.views import get_menu, get_restaurant_list_by_geo, get_restaurant,\
    get_recommended_dishes, restaurant_rating, get_restaurant_tags,\
    get_restaurants_with_tag, get_regions, get_restaurants_in_region, restaurantList,\
    get_order_by_id, get_user_profile, favorite_restaurant, favorite_restaurants,\
    get_following, remove_following, followers,\
    get_recommended_following, messages,\
    meal_participants, view_or_send_meal_invitations,\
    accept_or_reject_meal_invitations, img_test, upload_app
from grubcat.eo.views import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
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
    ('^api/v1/login/$', mobile_user_login),
    ('^api/v1/logout/$', mobile_user_logout),
    ('^order/$', get_orders),
    ('^order/(\d+)/$', get_order_by_id),
    ('^profile/$', get_user_profile),
    ('^profile/favorite/restaurant/(\d+)/$', favorite_restaurant),
    ('^profile/favorite/restaurant/$', favorite_restaurants),
    ('^search/restaurant/$', query_restaurant_from_google),

    #social
    ('^user/(\d+)/$', get_user_profile),
    ('^user/(\d+)/following/$', get_following),
    ('^user/(\d+)/following/remove/$', remove_following),
    ('^user/(\d+)/followers/$', followers),
    ('^user/(\d+)/following/recommendations/$', get_recommended_following),
    ('^user/(\d+)/messages/$', messages),
    #    ('^meal/$', get_meals),
    #   ('^meal/(\d+)/$', get_meal),
    ('^meal/(\d+)/participants/$', meal_participants),
    ('^user/(\d+)/invitation/$', view_or_send_meal_invitations),
    ('^user/(\d+)/invitation/(\d+)/$', accept_or_reject_meal_invitations),

    # developer interfaces...
    ('^updateLatLng/$', updateLatLng),
    ('^img_test/$', img_test),
    ('^upload_app/$', upload_app),

    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    ######################below is used for website urls
    # meal
    url(r'^$', MealListView.as_view(), name="index"),
    url(r'^meal/$', MealListView.as_view(), name="meal_list"),
    url(r'^meal/(?P<pk>\d+)/$', DetailView.as_view(
        model=Meal, context_object_name="meal", template_name="meal/meal_detail.html"), name='meal_detail'),

    # order
    url(r'^meal/(?P<meal_id>\d+)/order/$', login_required(OrderCreateView.as_view()), name='make_order'),
    url(r'^meal/(?P<meal_id>\d+)/order/(?P<pk>\d+)/$', login_required(OrderDetailView.as_view()), name='order_detail'),


    #account
    url(r'^user/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^user/logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),
    url(r'^user/register/$', RegisterView.as_view(), name='register'),
    url(r'^user/$', UserListView.as_view(), name="user_list"),
    url(r'^user/p/(?P<page>[0-9]+)/$', UserListView.as_view(template_name="user/user_container.html"),
        name="more_user"),

    #restaurant admin
    url(r'^restaurant/$', restaurant_login_required(TemplateView.as_view(template_name="restaurant/index.html")),
        name="restaurant_admin"),
    url(r'^restaurant/chekin/$', restaurant_login_required(CheckInFormView.as_view()), name="restaurant_admin_checkin"),
    url(r'^restaurant/chekin/result/$',
        restaurant_login_required(TemplateView.as_view(template_name="restaurant/checkin_result.html")),
        name="restaurant_admin_checkin_result"),
    url(r'^restaurant/menu/$', restaurant_login_required(TemplateView.as_view(template_name="restaurant/menu.html")),
        name="restaurant_admin_menu"),
    url(r'^restaurant/order/$', restaurant_login_required(TemplateView.as_view(template_name="restaurant/order.html")),
        name="restaurant_admin_order")
    ,
    #    url(r'^restaurant/login/$', TemplateView.as_view(template_name="restaurant/menu.html"),name="restaurant_admin_menu"),
    #    url(r'^restaurant/logout/$', TemplateView.as_view(template_name="restaurant/menu.html"),name="restaurant_admin_menu"),

    #support
    (r'^support/$', TemplateView.as_view(template_name="support/support.html")),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()



# Standard bits...
urlpatterns += patterns('',
    (r'^api/', include(v1_api.urls)),
)
