from django.conf.urls.defaults import *
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView
from eo.apis import v1_api, mobile_user_login, mobile_user_logout, mobile_user_register, weibo_user_login, checkemail
from eo.decorators import restaurant_login_required
from eo.views import  upload_app
from eo.views_common import list_tags, add_tag
from grubcat.eo.views import *
from django.conf import settings

import eo.views_restaurant as rest

admin.autodiscover()
urlpatterns = patterns('',
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    #    ('^get_restaurant_list_by_geo/$', get_restaurant_list_by_geo),
    #    ('^restaurant/(\d+)/$', get_restaurant),
    #    ('^restaurant/(\d+)/dish/recommendation/$', get_recommended_dishes),
    #    ('^restaurant/(\d+)/rating/$', restaurant_rating),
    #    ('^restaurant_tag/$', get_restaurant_tags),
    #    ('^restaurant_tag/(\d+)/restaurant/$', get_restaurants_with_tag),
    #    ('^region/$', get_regions),
    #    ('^region/(\d+)/restaurant/$', get_restaurants_in_region),
    #    ('^search_restaurant_list/$', restaurantList),
    ('^api/v1/login/$', mobile_user_login),
    ('^api/v1/logout/$', mobile_user_logout),
    ('^api/v1/weibo_user_login/$', weibo_user_login),
    ('^api/v1/checkemail/$', checkemail),
    ('^api/v1/register/$', mobile_user_register),
    #    ('^order/$', get_orders),
    #    ('^profile/$', get_user_profile),
    #    ('^profile/favorite/restaurant/(\d+)/$', favorite_restaurant),
    #    ('^profile/favorite/restaurant/$', favorite_restaurants),
    #    ('^search/restaurant/$', query_restaurant_from_google),

    #social
    #    ('^user/(\d+)/following/$', get_following),
    #    ('^user/(\d+)/following/remove/$', remove_following),
    #    ('^user/(\d+)/followers/$', followers),
    #    ('^user/(\d+)/following/recommendations/$', get_recommended_following),
    #    ('^user/(\d+)/messages/$', messages),
    #    ('^meal/(\d+)/participants/$', meal_participants),
    #    ('^user/(\d+)/invitation/$', view_or_send_meal_invitations),
    #    ('^user/(\d+)/invitation/(\d+)/$', accept_or_reject_meal_invitations),



    ######################below is used for website urls
    # meal
    url(r'^$', MealListView.as_view(), name="index"),
    url(r'^meal/$', MealListView.as_view(), name="meal_list"),
    url(r'^meal/(?P<meal_id>\d+)/$', MealDetailView.as_view(), name='meal_detail'),
    url(r'^meal/add/$', login_required(MealCreateView.as_view()), name='create_meal'),

    url(r'^user/(?P<user_id>\d+)/meals/$', UserMealListView.as_view(), name="user_meal_list"),


    #menu
    url(r'^menu/$', login_required(MenuListView.as_view()), name="menu_list"),
    url(r'^menu/(?P<pk>\d+)/$', login_required(MenuDetailView.as_view()), name="menu_detail"),

    #ajax get menus
    #    url(r'^menu/$',login_required(get_menu), name='get_menu'),

    #comment

    #group
    #    url(r'^group/$', GroupListView.as_view(), name="group_list"),
    #    url(r'^group/(?P<pk>\d+)/$', GroupDetailView.as_view(), name='group_detail'),
    #    url(r'^group/add/$',login_required(GroupCreateView.as_view()), name='create_group'),
    #    url(r'^group/edit/(?P<pk>\d+)/$',login_required(GroupUpdateView.as_view()), name='edit_group'),
    #    url(r'^group/logo/edit/(?P<pk>\d+)/$',login_required(GroupLogoUpdateView.as_view()), name='edit_group_logo'),
    #    url(r'^group/(?P<pk>\d+)/join/$',login_required(join_group), name='join_group'),
    #    url(r'^group/(?P<pk>\d+)/leave/$',login_required(leave_group), name='leave_group'),
    #    url(r'^group/comment/add/$',login_required(create_group_comment), name='create_group_comment'),
    #    url(r'^group/comment/(?P<pk>\d+)/del/$',login_required(del_group_comment), name='del_group_comment'),
    #    url(r'^group/(?P<group_id>\d+)/comment/p/(?P<page>[0-9]+)/$', GroupCommentListView.as_view(),
    #        name='group_comment_list'),
    #    url(r'^group/(?P<group_id>\d+)/member/$', GroupMemberListView.as_view(), name='group_member_list'),
    #    url(r'^group/(?P<group_id>\d +)/member/p/(?P<page>[0-9]+)/$', GroupMemberListView.as_view(template_name="group/member_container.html"), name='more_group_member_list'),

    # order
    #    url(r'^meal/(?P<meal_id>\d+)/order/$',login_required(OrderCreateView.as_view()), name='create_order'),
    url(r'^meal/(?P<meal_id>\d+)/order/(?P<pk>\d+)/$', login_required(OrderDetailView.as_view()),
        name='order_detail'),
    url(r'^order/paying/(?P<order_id>\d+)/$', login_required(pay_order),
        name='pay_order'),
    url(r'^meal/(?P<meal_id>\d+)/order/status/', login_required(check_order_status), name="check_order_status"),

    url(r'^login/weibo/$', weibo_login, name='weibo_login'),
#    url(r'^bind/$', login_required(BindProfileView.as_view()), name='bind'),
    url(r'^user/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^user/logout/$', 'django.contrib.auth.views.logout_then_login', kwargs={'login_url': "/"}, name="logout"),


    #account
    #    url(r'^user/register/$', RegisterView.as_view(), name='register'),
    url(r'^user/$', UserListView.as_view(), name="user_list"),
    url(r'^user/p/(?P<page>[0-9]+)/$', UserListView.as_view(template_name="user/user_container.html"),
        name="more_user"),
    url(r'^profile/edit/$', login_required(ProfileUpdateView.as_view()), name='edit_basic_profile'),
    url(r'^user/(?P<pk>\d+)/$', login_required(ProfileDetailView.as_view()), name='user_detail'),
    url(r'profile/upload_avatar/$', login_required(UploadAvatarView.as_view()), name='upload_avatar'),
    url(r'user/info/$', login_required(get_user_info), name='get_user_info'),


    url(r'^follow/(?P<user_id>\d+)/$', login_required(follow), name='follow'),
    url(r'^unfollow/(?P<user_id>\d+)/$', login_required(un_follow), name='un_follow'),
    url(r'^follows/(?P<user_id>\d+)/$', login_required(FollowsView.as_view()), name='following_list'),

    #photo
    url(r'^photo/u/(?P<user_id>\d+)/$', login_required(PhotoListView.as_view()), name='photo_list'),
    url(r'^photo/upload/$', login_required(PhotoCreateView.as_view()), name='upload_photo'),
    url(r'^photo/(?P<pk>\d+)/$', login_required(PhotoDetailView.as_view()), name='photo_detail'),
    url(r'^photo/del/(?P<pk>\d+)/$', login_required(del_photo), name='del_photo'),

    url(r'^tag/$', login_required(list_tags), name='tag_list'),
    url(r'^tag/add/$', login_required(add_tag), name='add_tag'),

    #restaurant admin
    url(r'^restaurant/$', restaurant_login_required(rest.OrderCheckInView.as_view()), name="restaurant_admin"),

    url(r'^restaurant/chekin/$', restaurant_login_required(rest.OrderCheckInView.as_view()),
        name="restaurant_checkin"),
    url(r'^restaurant/order/use/$', restaurant_login_required(rest.use_order), name="restaurant_use_order"),

    url(r'^restaurant/order/today/$', restaurant_login_required(rest.TodayMealListView.as_view()), name="restaurant_today_meals"),


    url(r'^restaurant/dish/$', restaurant_login_required(rest.DishListView.as_view()), name="restaurant_dish_list"),
    url(r'^restaurant/dish/add/$', restaurant_login_required(rest.DishCreateView.as_view()),
        name="restaurant_dish_add"),
    url(r'^restaurant/dish/edit/(?P<pk>\d+)/$', restaurant_login_required(rest.DishUpdateView.as_view()),
        name="restaurant_dish_edit"),
    url(r'^restaurant/dish/del/(?P<pk>\d+)/$', restaurant_login_required(rest.DishDeleteView.as_view()),
        name="restaurant_dish_del"),
    url(r'^restaurant/dish_category/add/$', restaurant_login_required(rest.add_dish_category),
        name="add_dish_category"),

    url(r'^restaurant/order/$',
        restaurant_login_required(TemplateView.as_view(template_name="restaurant/order_history.html")),
        name="restaurant_order"),

    url(r'^restaurant/menu/$', restaurant_login_required(rest.MenuListView.as_view()), name="restaurant_menu_list"),
    url(r'^restaurant/menu/add/$', restaurant_login_required(rest.add_menu), name="add_menu"),
    url(r'^restaurant/menu/del/(?P<pk>\d+)/$', restaurant_login_required(rest.del_menu), name="del_menu"),
    url(r'^restaurant/menu/edit/(?P<pk>\d+)/$', restaurant_login_required(rest.edit_menu), name="edit_menu"),
    url(r'^restaurant/menu/copy/(?P<pk>\d+)/$', restaurant_login_required(rest.copy_menu), name="copy_menu"),
    url(r'^restaurant/menu/cover/edit/(?P<pk>\d+)/$', restaurant_login_required(rest.EditMenuCoverView.as_view()),
        name="edit_menu_cover"),

    #chat
    url(r'^chat/$', TemplateView.as_view(template_name="chat.html"), name="chat"),

    #support
    url(r'^support/$', TemplateView.as_view(template_name="support/support.html"), name="support"),
    (r'^test/$', TemplateView.as_view(template_name="test.html")),

    # developer interfaces...
    ('^upload_app/$', upload_app),

    #pay
    url(r'^pay/alipay/back/sync/$', handle_back_sync, name="alipay_back_sync"),
    url(r'^pay/alipay/back/async/$', handle_back_aysnc, name="alipay_back_async"),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()



# Standard bits...
urlpatterns += patterns('',
    (r'^api/', include(v1_api.urls)),
)
