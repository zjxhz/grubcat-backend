from django import template
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static

register = template.Library()

static_url = settings.STATIC_URL
if not static_url.endswith("/"):
    static_url += "/"

@register.simple_tag
def static_asset(path):
    """
    this tag is only used as below,
     {% assets "meal_list_css" %}
        <link href="{% static_asset ASSET_URL %}" media="screen" rel="stylesheet" type="text/css">
    {% endassets %}
    The reason is to use webassets to compress js/css files and use static of cachedstaticfilestorage to add hash name in a static file name.
    The ASSET_URL will be STATIC_URL+file relative name, such as /static/css/a.css, but static tag only accept  url relative to STATIC_URL.
     This tag is to remove the STATIC_URL in the ASSET_URL and then use static tags to add a hash in the file name.
    """
    if path.startswith(static_url):
        path = path.replace(static_url, "", len(static_url))
    return static(path)
