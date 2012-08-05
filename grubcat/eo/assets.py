from django.conf import settings
from django_assets import Bundle, register, env
#env.directory=settings.STATIC_ROOT
#env.url_expire = True
import django_assets
from webassets.env import Environment

#css below

base_css = Bundle('css/base.css', filters='cssmin', output='gen/css/base.%(version)s.css')
form_css = Bundle('less/form.less',filters='less',output='gen/css/form.%(version)s.css',debug=False)
common_css = Bundle('css/common.css',form_css, filters='cssmin', output='gen/css/common.%(version)s.css')
dropkick_css = Bundle('css/dropkick.css', filters='cssmin',output='gen/css/dropkick.%(version)s.css')

bootstrap_css = Bundle(
    'css/bootstrap.css', filters='cssmin', output='gen/css/bootstrap.%(version)s.css'
)

meal_list_css = Bundle(
    base_css, common_css,dropkick_css, 'css/meal-list.css', filters='cssmin', output='gen/css/meal-list.%(version)s.css'
)
meal_detail_css = Bundle(
    base_css, common_css, 'css/meal-detail.css', filters='cssmin', output='gen/css/meal-detail.%(version)s.css'
)

account_css = Bundle(
    base_css, common_css, 'css/account.css', filters='cssmin', output='gen/css/account.%(version)s.css'
)

user_list_css = Bundle(
    base_css,  common_css, 'css/user-list.css', filters='cssmin', output='gen/css/user-list.%(version)s.css'
)

order_css = Bundle(
    base_css, bootstrap_css, common_css, 'css/order.css', filters='cssmin', output='gen/css/order.%(version)s.css'
)

restaurant_admin_css = Bundle(
    'css/restaurant-admin.css', filters='cssmin', output='gen/css/restaurant-admin.%(version)s.css'
)

#js below
jquery_js = Bundle('js/jquery-1.7.2.min.js' ,output='gen/js/jquery-1.7.2.%(version)s.js')

base_js = Bundle( jquery_js, 'js/jquery.dropkick-1.0.0.js','js/common.js',filters='jsmin', output="gen/js/base.%(version)s.js")

user_list_js = Bundle(
    'js/user-list.js', filters='jsmin', output='gen/js/user-list.%(version)s.js'
)

restaurant_admin_js = Bundle(
    'js/restaurant-admin.js', filters='jsmin', output='gen/js/restaurant-admin.%(version)s.js'
)

fix_ie6_png_js = Bundle(
    'js/DD_belatedPNG_0.0.8a.js', filters='jsmin', output='gen/js/DD_belatedPNG_0.0.8a.%(version)s.js'
)

water_fall_js = Bundle(
    'js/jquery.infinitescroll.min.js', 'js/jquery.masonry.min.js', 'js/modernizr-transitions.js',
    output='gen/js/water-fall.%(version)s.js'
)
jquery_form_js = Bundle('js/jquery.form.js', filters='jsmin', output='gen/js/jquery.form.%(version)s.js')

jquery_ajax_bootstrap_js = Bundle(
    'js/jquery.controls.js', 'js/jquery.dialog2.js', 'js/jquery.dialog2.helpers.js', filters='jsmin',
    output='gen/js/jquery.ajax.bootstrap.js.%(version)s.js'
)

jquery_ui_js = Bundle('js/jquery-ui-1.8.21.custom.js', filters='jsmin', output='gen/js/jquery-ui-1.8.21.custom%(version)s.js')

register('base_css', base_css)
register('common_css', common_css)
register('form_css', form_css)
register('bootstrap_css', bootstrap_css)
register('meal_list_css', meal_list_css)
register('meal_detail_css', meal_detail_css)
register('account_css', account_css)
register('user_list_css', user_list_css)
register('order_css', order_css)
register('restaurant_admin_css', restaurant_admin_css)

register('jquery_js', jquery_js)
register('base_js', base_js)
register('restaurant_admin_js', restaurant_admin_js)
register('user_list_js', user_list_js)
register('fix_ie6_png_js', fix_ie6_png_js)
register('water_fall_js', water_fall_js)
register('jquery_form_js', jquery_form_js)
register('jquery_ajax_bootstrap_js', jquery_ajax_bootstrap_js)
register('jquery_ui_js', jquery_ui_js)

