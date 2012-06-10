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

dd_fixPNG_js = Bundle(
    'js/DD_belatedPNG_0.0.8a.js', filters='jsmin', output='gen/DD_belatedPNG_0.0.8a.%(version)s.js'
)

register('base_css', base_css)
register('meal_list_css', meal_list_css)
register('meal_detail_css', meal_detail_css)
register('dd_fixPNG_js', dd_fixPNG_js)
