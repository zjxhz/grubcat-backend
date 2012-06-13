from django.conf import settings
from django_assets import Bundle, register, env
#env.directory=settings.STATIC_ROOT
#env.url_expire = True
import django_assets
from webassets.env import Environment

base_css = Bundle('css/base.css', filters='cssmin', output='gen/base.%(version)s.css')
meal_list_css = Bundle(
    'css/base.css', 'css/meal-list.css', filters='cssmin', output='gen/meal-list.%(version)s.css'
)
meal_detail_css = Bundle(
    'css/base.css', 'css/meal-detail.css', filters='cssmin', output='gen/meal-detail.%(version)s.css'
)

account_css = Bundle(
    'css/base.css', 'css/account.css', filters='cssmin', output='gen/account.%(version)s.css'
)

user_list_css = Bundle(
    'css/base.css', 'css/user-list.css', filters='cssmin', output='gen/user-list.%(version)s.css'
)

user_list_js = Bundle(
    'js/user-list.js', filters='jsmin', output='gen/user-list.%(version)s.js'
)

fix_ie6_png_js = Bundle(
    'js/DD_belatedPNG_0.0.8a.js', filters='jsmin', output='gen/DD_belatedPNG_0.0.8a.%(version)s.js'
)

water_fall_js = Bundle(
    'js/jquery.infinitescroll.min.js', 'js/jquery.masonry.min.js', 'js/modernizr-transitions.js',
    output='gen/water_fall.%(version)s.js'
)

register('base_css', base_css)
register('meal_list_css', meal_list_css)
register('meal_detail_css', meal_detail_css)
register('account_css', account_css)
register('user_list_css', user_list_css)

register('user_list_js', user_list_js)
register('fix_ie6_png_js', fix_ie6_png_js)
register('water_fall_js', water_fall_js)
