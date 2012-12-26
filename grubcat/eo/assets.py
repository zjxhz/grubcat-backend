from django.conf import settings
from django_assets import Bundle, register, env
#env.directory=settings.STATIC_ROOT
#env.url_expire = True
import django_assets
from webassets.env import Environment

#css below
bootstrap_css = Bundle(
    'less/bootstrap/bootstrap.less', filters='less,cssmin', output='gen/bootstrap.%(version)s.css', depends='less/bootstrap/*.less'
)
#bootstrap_main_css = Bundle(
#        'less/bootstrap/bootstrap-main.less', filters='less,cssmin', output='gen/bootstrap.%(version)s.css',
#)
#form_css = Bundle('less/form.less',filters='less',output='gen/form.%(version)s.css')
form_css = Bundle('css/form.css', filters='cssmin', output='gen/form.%(version)s.css')
common_css = Bundle('css/common.css', filters='cssmin', output='gen/common.%(version)s.css')
dropkick_css = Bundle('css/dropkick.css', filters='cssmin', output='gen/dropkick.%(version)s.css')

base_css = Bundle(bootstrap_css,   filters='cssmin', output='gen/base.%(version)s.css')

meal_css = Bundle(
   'css/common.css',  'less/meal.less', filters='less,cssmin', output='gen/meal.%(version)s.css'
)
meal_detail_css = Bundle(
    'css/common.css',  'css/meal-detail.css', filters='cssmin', output='gen/meal-detail.%(version)s.css'
)

meal_add_css = Bundle(
   dropkick_css, 'css/common.css', 'css/create-meal.css', filters='cssmin', output='gen/meal-add.%(version)s.css'
)

#group related
group_list_css = Bundle(
    dropkick_css, 'css/common.css', 'css/group-list.css', filters='cssmin', output='gen/group-list.%(version)s.css'
)
group_detail_css = Bundle(
    dropkick_css, 'css/common.css', 'css/group-detail.css', filters='cssmin', output='gen/group-detail.%(version)s.css'
)

#user related
account_css = Bundle(
    'css/common.css',   'css/account.css', filters='cssmin', output='gen/account.%(version)s.css'
)

user_list_css = Bundle(
    'css/common.css',  'css/user-list.css', filters='cssmin', output='gen/user-list.%(version)s.css'
)

edit_profile_css = Bundle(
    'css/common.css',   'css/edit-profile.css', filters='cssmin', output='gen/edit-profile.%(version)s.css'
)

order_css = Bundle(
     dropkick_css, 'css/common.css',  'css/order.css', filters='cssmin', output='gen/order.%(version)s.css'
)

restaurant_admin_css = Bundle(
    'css/common.css', 'css/restaurant-admin.css', filters='cssmin', output='gen/restaurant-admin.%(version)s.css'
)

#js below
jquery_js = Bundle('js/jquery-1.7.2.min.js', output='gen/jquery-1.7.2.%(version)s.js')

jquery_dropkick_js = Bundle('js/jquery.dropkick-1.0.0.js', output='gen/jquery-dropkick.%(version)s.js', filters='jsmin')

base_js = Bundle(jquery_js, jquery_dropkick_js, 'js/bootstrap.min.js',
    output="gen/base.%(version)s.js")

base_main_js = Bundle(jquery_js, 'js/bootstrap.min.js', 'js/jquery.lazyload.min.js', filters='jsmin',
    output="gen/base.main.%(version)s.js")

user_list_js = Bundle(
    'js/user-list.js', filters='jsmin', output='gen/user-list.%(version)s.js'
)

restaurant_admin_js = Bundle(
    'js/restaurant-admin.js', filters='jsmin', output='gen/restaurant-admin.%(version)s.js'
)

#fix_ie6_png_js = Bundle(
#    'js/DD_belatedPNG_0.0.8a.js', filters='jsmin', output='gen/DD_belatedPNG_0.0.8a.%(version)s.js'
#)

water_fall_js = Bundle(
    'js/jquery.infinitescroll.min.js', 'js/jquery.masonry.min.js', 'js/modernizr-transitions.js',
    output='gen/water-fall.%(version)s.js'
)
jquery_form_js = Bundle('js/jquery.form.js', filters='jsmin', output='gen/jquery.form.%(version)s.js')

jquery_ajax_bootstrap_js = Bundle(
    'js/jquery.controls.js', 'js/jquery.dialog2.js', 'js/jquery.dialog2.helpers.js', filters='jsmin',
    output='gen/jquery.ajax.bootstrap.js.%(version)s.js'
)

jquery_ui_js = Bundle('js/jquery-ui-1.8.21.custom.js', filters='jsmin',
    output='gen/jquery-ui-1.8.21.custom%(version)s.js')

image_cropping_js = Bundle(jquery_js, 'js/jquery.Jcrop.js', 'js/image_cropping.js', filters='jsmin',
    output='gen/iamge-cropping%(version)s.js')

register('common_css', common_css)
register('base_css', base_css)
register('form_css', form_css)
register('bootstrap_css', bootstrap_css)
register('dropkick_css', dropkick_css)
register('meal_css', meal_css)
register('meal_detail_css', meal_detail_css)
register('meal_add_css', meal_add_css)
register('group_list_css', group_list_css)
register('group_detail_css', group_detail_css)

register('account_css', account_css)
register('user_list_css', user_list_css)
register('edit_profile_css', edit_profile_css)
register('order_css', order_css)
register('restaurant_admin_css', restaurant_admin_css)

register('jquery_js', jquery_js)
register('base_js', base_js)
register('base_main_js', base_main_js)
register('restaurant_admin_js', restaurant_admin_js)
register('user_list_js', user_list_js)
#register('fix_ie6_png_js', fix_ie6_png_js)
register('water_fall_js', water_fall_js)
register('jquery_form_js', jquery_form_js)
register('jquery_ajax_bootstrap_js', jquery_ajax_bootstrap_js)
register('jquery_ui_js', jquery_ui_js)
register('image_cropping_js', image_cropping_js)

