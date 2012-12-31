from django.conf import settings
from django_assets import Bundle, register, env
#env.directory=settings.STATIC_ROOT
#env.url_expire = True
import django_assets
from webassets.env import Environment

#css below
bootstrap_css = Bundle(
    'less/bootstrap/bootstrap.less','less/bootstrap/responsive.less', filters='less,cssmin', output='gen/bootstrap.css', depends='less/bootstrap/*.less'
)
#bootstrap_main_css = Bundle(
#        'less/bootstrap/bootstrap-main.less', filters='less,cssmin', output='gen/bootstrap.css',
#)
#form_css = Bundle('less/form.less',filters='less',output='gen/form.css')
form_css = Bundle('css/form.css', filters='cssmin', output='gen/form.css')
common_css = Bundle('less/common.less', filters='less,cssmin', output='gen/common.css')
dropkick_css = Bundle('css/dropkick.css', filters='cssmin', output='gen/dropkick.css')

base_css = Bundle(bootstrap_css,   filters='cssmin', output='gen/base.css')

meal_css = Bundle(
   common_css,  'less/meal.less', filters='less,cssmin', output='gen/meal.css'
)

meal_add_css = Bundle(
   dropkick_css, common_css, 'css/create-meal.css', filters='cssmin', output='gen/meal-add.css'
)

#group related
group_list_css = Bundle(
    dropkick_css, common_css, 'css/group-list.css', filters='cssmin', output='gen/group-list.css'
)
group_detail_css = Bundle(
    dropkick_css, common_css, 'css/group-detail.css', filters='cssmin', output='gen/group-detail.css'
)

#user related
account_css = Bundle(
    common_css,   'css/account.css', filters='cssmin', output='gen/account.css'
)

user_list_css = Bundle(
    common_css,  'css/user-list.css', filters='cssmin', output='gen/user-list.css'
)

user_css = Bundle(
    common_css,  filters='cssmin', output='gen/user.css'
)

edit_profile_css = Bundle(
    common_css,   'css/edit-profile.css', filters='cssmin', output='gen/edit-profile.css'
)

order_css = Bundle(
     dropkick_css, common_css,  'css/order.css', filters='cssmin', output='gen/order.css'
)

restaurant_admin_css = Bundle(
     'less/restaurant-admin.less', filters='less,cssmin', output='gen/restaurant-admin.css'
)

#js below
jquery_js = Bundle('js/jquery-1.7.2.min.js', output='gen/jquery-1.7.2.js')

jquery_dropkick_js = Bundle('js/jquery.dropkick-1.0.0.js', output='gen/jquery-dropkick.js', filters='jsmin')

base_js = Bundle(jquery_js, jquery_dropkick_js, 'js/bootstrap.min.js',
    output="gen/base.js")

base_main_js = Bundle(jquery_js, 'js/bootstrap.min.js', 'js/jquery.lazyload.min.js', filters='jsmin',
    output="gen/base.main.js")

user_list_js = Bundle(
    'js/user-list.js', filters='jsmin', output='gen/user-list.js'
)

restaurant_admin_js = Bundle(
    'js/restaurant-admin.js', filters='jsmin', output='gen/restaurant-admin.js'
)

#fix_ie6_png_js = Bundle(
#    'js/DD_belatedPNG_0.0.8a.js', filters='jsmin', output='gen/DD_belatedPNG_0.0.8a.js'
#)

water_fall_js = Bundle(
    'js/jquery.infinitescroll.min.js', 'js/jquery.masonry.min.js', 'js/modernizr-transitions.js',
    output='gen/water-fall.js'
)
jquery_form_js = Bundle('js/jquery.form.js', filters='jsmin', output='gen/jquery.form.js')

jquery_ajax_bootstrap_js = Bundle(
    'js/jquery.controls.js', 'js/jquery.dialog2.js', 'js/jquery.dialog2.helpers.js', filters='jsmin',
    output='gen/jquery.ajax.bootstrap.js.js'
)

jquery_ui_js = Bundle('js/jquery-ui-1.8.21.custom.js', filters='jsmin',
    output='gen/jquery-ui-1.8.21.customjs')

image_cropping_js = Bundle(jquery_js, 'js/jquery.Jcrop.js', 'js/image_cropping.js', filters='jsmin',
    output='gen/iamge-croppingjs')

register('common_css', common_css)
register('base_css', base_css)
register('form_css', form_css)
register('bootstrap_css', bootstrap_css)
register('dropkick_css', dropkick_css)
register('meal_css', meal_css)
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

