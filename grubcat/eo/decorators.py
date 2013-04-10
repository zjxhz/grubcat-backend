import django
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import json
try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.

from django.contrib.auth import REDIRECT_FIELD_NAME

def ajax_login_required(view_func):
    @wraps(view_func)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        result = json.dumps({ 'not_authenticated': True })
        return HttpResponse(result, mimetype='application/json')
    return wrap

def restaurant_login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    if not login_url:
        login_url = django.conf.settings.RESTAURANT_LOGIN_URL
    actual_decorator = user_passes_test(
        test_restaurant_user,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

#def active_login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
#    """
#    Decorator for views that checks that the user is logged in, redirecting
#    to the log-in page if necessary.
#    """
#    actual_decorator = user_passes_test(
#        lambda u: u.is_authenticated() and u.is_active,
#        login_url=login_url,
#        redirect_field_name=redirect_field_name
#    )
#    if function:
#        return actual_decorator(function)
#    return actual_decorator


def test_restaurant_user(user):
    if user.is_authenticated():
        try:
            restaurant = user.restaurant
            return True
        except ObjectDoesNotExist: pass
    return False

