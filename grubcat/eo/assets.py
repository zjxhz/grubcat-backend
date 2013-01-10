from django.conf import settings
from django_assets import Bundle, register, env
#env.directory=settings.STATIC_ROOT
#env.url_expire = True
import django_assets
from webassets.env import Environment

#css below
bootstrap_css = Bundle(
    'less/bootstrap/bootstrap.less', 'less/bootstrap/responsive.less', filters='less,cssmin',
    output='gen/bootstrap.%(version)s.css', depends='less/bootstrap/*.less'
)
dropkick_css = Bundle('css/dropkick.css', filters='cssmin', output='gen/dropkick.%(version)s.css')
common_css = Bundle(dropkick_css, 'less/common.less',filters='less,cssmin', output='gen/common.%(version)s.css')
responsive_css = Bundle( 'less/responsive.less',filters='less,cssmin', output='gen/responsive.%(version)s.css')

base_css = Bundle(bootstrap_css, filters='cssmin', output='gen/base.%(version)s.css')

meal_css = Bundle(
    common_css, 'less/meal.less', responsive_css, filters='less,cssmin', output='gen/meal.%(version)s.css'
)

error_css = Bundle(
    common_css, responsive_css, output='gen/error.%(version)s.css'
)

#group related
#group_list_css = Bundle(
#     common_css, 'css/group-list.css', filters='cssmin', output='gen/group-list.%(version)s..css'
#)
#group_detail_css = Bundle(
#     common_css, 'css/group-detail.css', filters='cssmin', output='gen/group-detail.%(version)s.css'
#)

#user related
account_css = Bundle(
    common_css, 'css/account.css',responsive_css,  filters='cssmin', output='gen/account.%(version)s.css'
)

user_list_css = Bundle(
    common_css, 'less/user-list.less',responsive_css,  filters='less, cssmin', output='gen/user-list.%(version)s.css'
)

user_css = Bundle(
    common_css, responsive_css,  filters='cssmin', output='gen/user.%(version)s.css'
)

edit_profile_css = Bundle(
    'css/jquery.Jcrop.css','css/autoSuggest.css',common_css ,'less/edit-profile.less', responsive_css, filters='less,cssmin', output='gen/edit-profile.%(version)s.css'
)

#order_css = Bundle(
#     common_css, 'css/order.css', filters='cssmin', output='gen/order.%(version)s.css'
#)

restaurant_admin_css = Bundle(
    'less/restaurant-admin.less',responsive_css,  filters='less,cssmin', output='gen/restaurant-admin.%(version)s.css'
)

#js below
jquery_js = Bundle('js/jquery-1.7.2.min.js', output='gen/jquery-1.7.2.%(version)s.js')

jquery_dropkick_js = Bundle('js/jquery.dropkick-1.0.0.js', output='gen/jquery-dropkick.%(version)s.js', filters='jsmin')

base_js = Bundle(jquery_js, 'js/bootstrap.min.js',
    output="gen/base.%(version)s.js")

base_main_js = Bundle(jquery_js, 'js/bootstrap.min.js', 'js/jquery.lazyload.min.js', filters='jsmin',
    output="gen/base.main.%(version)s.js")

module_js = Bundle('js/module.js', filters='jsmin', output="gen/module.%(version)s.js")
auto_suggest_js = Bundle('js/jquery.autoSuggest.js', filters='jsmin', output="gen/autosuggest.%(version)s.js")

water_fall_js = Bundle(
    'js/jquery.infinitescroll.min.js', 'js/jquery.masonry.min.js', 'js/modernizr-transitions.js',
    output='gen/water-fall.%(version)s.js'
)
user_list_js = Bundle(
    water_fall_js, 'js/user-list.js', filters='jsmin', output='gen/user-list.%(version)s.js'
)

restaurant_admin_js = Bundle(
    'js/restaurant-admin.js', filters='jsmin', output='gen/restaurant-admin.%(version)s.js'
)

#fix_ie6_png_js = Bundle(
#    'js/DD_belatedPNG_0.0.8a.js', filters='jsmin', output='gen/DD_belatedPNG_0.0.8a.js'
#)


jquery_form_js = Bundle('js/jquery.form.js', filters='jsmin', output='gen/jquery.form.%(version)s.js')

jquery_ajax_bootstrap_js = Bundle(
    'js/jquery.controls.js', 'js/jquery.dialog2.js', 'js/jquery.dialog2.helpers.js', filters='jsmin',
    output='gen/jquery.ajax.bootstrap.%(version)s.js'
)

jquery_ui_js = Bundle('js/jquery-ui-1.8.21.custom.js', filters='jsmin',
    output='gen/jquery-ui-1.8.21.custom.%(version)s.js')

image_cropping_js = Bundle( 'js/jquery.Jcrop.js', 'js/image_cropping.js', filters='jsmin',
    output='gen/iamge-cropping.%(version)s.js')

register('common_css', common_css)
register('base_css', base_css)
register('bootstrap_css', bootstrap_css)
register('dropkick_css', dropkick_css)
register('meal_css', meal_css)
#register('group_list_css', group_list_css)
#register('group_detail_css', group_detail_css)

register('error_css', error_css)
register('account_css', account_css)
register('user_list_css', user_list_css)
register('edit_profile_css', edit_profile_css)
#register('order_css', order_css)
register('restaurant_admin_css', restaurant_admin_css)

register('jquery_js', jquery_js)
register('jquery_dropkick_js', jquery_dropkick_js)
register('base_js', base_js)
register('base_main_js', base_main_js)
register('module_js', module_js)
register('auto_suggest_js', auto_suggest_js)
register('restaurant_admin_js', restaurant_admin_js)
register('user_list_js', user_list_js)
#register('fix_ie6_png_js', fix_ie6_png_js)
register('water_fall_js', water_fall_js)
register('jquery_form_js', jquery_form_js)
register('jquery_ajax_bootstrap_js', jquery_ajax_bootstrap_js)
register('jquery_ui_js', jquery_ui_js)
register('image_cropping_js', image_cropping_js)

