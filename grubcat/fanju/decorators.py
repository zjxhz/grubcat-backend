import django
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import json
from django.middleware.cache import CacheMiddleware
from django.utils.decorators import decorator_from_middleware_with_args

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


class CacheMdidlewareForAnonymous(CacheMiddleware):
    def process_request(self, request):
        if request.user.is_authenticated():
            request._cache_update_cache = False
            return None
        else:
            return super(CacheMdidlewareForAnonymous, self).process_request(request)


def cache_page_for_anonymous(*args, **kwargs):
    """
    Decorator for views that tries getting the page from the cache and
    populates the cache if the page isn't in the cache yet.

    The cache is keyed by the URL and some data from the headers.
    Additionally there is the key prefix that is used to distinguish different
    cache areas in a multi-site setup. You could use the
    sites.get_current_site().domain, for example, as that is unique across a Django
    project.

    Additionally, all headers from the response's Vary header will be taken
    into account on caching -- just like the middleware does.
    """
    # We need backwards compatibility with code which spells it this way:
    #   def my_view(): pass
    #   my_view = cache_page(my_view, 123)
    # and this way:
    #   my_view = cache_page(123)(my_view)
    # and this:
    #   my_view = cache_page(my_view, 123, key_prefix="foo")
    # and this:
    #   my_view = cache_page(123, key_prefix="foo")(my_view)
    # and possibly this way (?):
    #   my_view = cache_page(123, my_view)
    # and also this way:
    #   my_view = cache_page(my_view)
    # and also this way:
    #   my_view = cache_page()(my_view)

    # We also add some asserts to give better error messages in case people are
    # using other ways to call cache_page that no longer work.
    cache_alias = kwargs.pop('cache', None)
    key_prefix = kwargs.pop('key_prefix', None)
    assert not kwargs, "The only keyword arguments are cache and key_prefix"
    def warn():
        import warnings
        warnings.warn('The cache_page decorator must be called like: '
                      'cache_page(timeout, [cache=cache name], [key_prefix=key prefix]). '
                      'All other ways are deprecated.',
                      DeprecationWarning,
                      stacklevel=2)

    if len(args) > 1:
        assert len(args) == 2, "cache_page accepts at most 2 arguments"
        warn()
        if callable(args[0]):
            return decorator_from_middleware_with_args(CacheMdidlewareForAnonymous)(cache_timeout=args[1], cache_alias=cache_alias, key_prefix=key_prefix)(args[0])
        elif callable(args[1]):
            return decorator_from_middleware_with_args(CacheMdidlewareForAnonymous)(cache_timeout=args[0], cache_alias=cache_alias, key_prefix=key_prefix)(args[1])
        else:
            assert False, "cache_page must be passed a view function if called with two arguments"
    elif len(args) == 1:
        if callable(args[0]):
            warn()
            return decorator_from_middleware_with_args(CacheMdidlewareForAnonymous)(cache_alias=cache_alias, key_prefix=key_prefix)(args[0])
        else:
            # The One True Way
            return decorator_from_middleware_with_args(CacheMdidlewareForAnonymous)(cache_timeout=args[0], cache_alias=cache_alias, key_prefix=key_prefix)
    else:
        warn()
        return decorator_from_middleware_with_args(CacheMdidlewareForAnonymous)(cache_alias=cache_alias, key_prefix=key_prefix)
