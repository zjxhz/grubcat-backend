import django
from django.conf.urls.defaults import *
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView
from eo.apis import v1_api, mobile_user_login, mobile_user_logout, mobile_user_register, weibo_user_login
from eo.db import query_restaurant_from_google, updateLatLng
from eo.decorators import restaurant_login_required
from eo.views import  get_restaurant_list_by_geo, get_restaurant,\
    get_recommended_dishes, restaurant_rating, get_restaurant_tags,\
    get_restaurants_with_tag, get_regions, get_restaurants_in_region, restaurantList,\
    get_order_by_id, get_user_profile, favorite_restaurant, favorite_restaurants,\
    get_following, remove_following, followers,\
    get_recommended_following, messages,\
    meal_participants, view_or_send_meal_invitations,\
    accept_or_reject_meal_invitations, img_test, upload_app
from grubcat.eo.views import *
from django.conf import settings

import eo.views_restaurant as rest

admin.autodiscover()
urlpatterns = patterns('',
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

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
    ('^api/v1/weibo_user_login/$', weibo_user_login),
    ('^api/v1/register/$', mobile_user_register),
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

    ######################below is used for website urls
    # meal
    url(r'^$', MealListView.as_view(), name="index"),
    url(r'^meal/$', MealListView.as_view(), name="meal_list"),
    url(r'^meal/(?P<pk>\d+)/$', MealDetailView.as_view(), name='meal_detail'),
    url(r'^meal/add/$', login_required(MealCreateView.as_view()), name='create_meal'),

    #menu
    url(r'^menu/$', login_required(MenuListView.as_view()), name="menu_list"),

    #ajax get menus
#    url(r'^menu/$', login_required(get_menu), name='get_menu'),

    #group
    url(r'^group/$', GroupListView.as_view(), name="group_list"),
    url(r'^group/(?P<pk>\d+)/$', GroupDetailView.as_view(), name='group_detail'),
    url(r'^group/add/$', login_required(GroupCreateView.as_view()), name='create_group'),
    url(r'^group/edit/(?P<pk>\d+)/$', login_required(GroupUpdateView.as_view()), name='edit_group'),
    url(r'^group/logo/edit/(?P<pk>\d+)/$', login_required(GroupLogoUpdateView.as_view()), name='edit_group_logo'),
    url(r'^group/(?P<pk>\d+)/join/$', login_required(join_group), name='join_group'),
    url(r'^group/(?P<pk>\d+)/leave/$', login_required(GroupLogoUpdateView.as_view()), name='leave_group'),

    # order
    url(r'^meal/(?P<meal_id>\d+)/order/$', login_required(OrderCreateView.as_view()), name='create_order'),
    url(r'^meal/(?P<meal_id>\d+)/order/(?P<pk>\d+)/$', login_required(OrderDetailView.as_view()), name='order_detail'),

    #account
    url(r'^user/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^user/logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),
    url(r'^user/register/$', RegisterView.as_view(), name='register'),
    url(r'^user/$', UserListView.as_view(), name="user_list"),
    url(r'^user/p/(?P<page>[0-9]+)/$', UserListView.as_view(template_name="user/user_container.html"),
        name="more_user"),

    #restaurant admin
    url(r'^restaurant/$', restaurant_login_required(rest.OrderCheckInView.as_view()), name="restaurant_admin"),

    url(r'^restaurant/chekin/$', restaurant_login_required(rest.OrderCheckInView.as_view()), name="restaurant_checkin"),
    url(r'^restaurant/order/use/$', restaurant_login_required(rest.use_order), name="restaurant_use_order"),

    url(r'^restaurant/dish/$', restaurant_login_required(rest.DishListView.as_view()), name="restaurant_dish_list"),
    url(r'^restaurant/dish/add/$', restaurant_login_required(rest.DishCreateView.as_view()), name="restaurant_dish_add"),
    url(r'^restaurant/dish/edit/(?P<pk>\d+)/$', restaurant_login_required(rest.DishUpdateView.as_view()),
        name="restaurant_dish_edit"),
    url(r'^restaurant/dish/del/(?P<pk>\d+)/$', restaurant_login_required(rest.DishDeleteView.as_view()),
        name="restaurant_dish_del"),
    url(r'^restaurant/dish_category/add/$', restaurant_login_required(rest.add_dish_category), name="add_dish_category"),

    url(r'^restaurant/order/$', restaurant_login_required(TemplateView.as_view(template_name="restaurant/order_history.html")),
        name="restaurant_order"),

    url(r'^restaurant/menu/$', restaurant_login_required(rest.MenuListView.as_view()), name="restaurant_menu_list"),
    url(r'^restaurant/menu/add/$', restaurant_login_required(rest.add_menu), name="add_menu"),
    url(r'^restaurant/menu/del/(?P<pk>\d+)/$', restaurant_login_required(rest.del_menu), name="del_menu"),
    url(r'^restaurant/menu/edit/(?P<pk>\d+)/$', restaurant_login_required(rest.edit_menu), name="edit_menu"),

    (r'^test/$', TemplateView.as_view(template_name="test.html")),

    #support
    url(r'^support/$', TemplateView.as_view(template_name="support/support.html"), name="support"),

)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()



# Standard bits...
urlpatterns += patterns('',
    (r'^api/', include(v1_api.urls)),
)
