#coding=utf-8
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from raven.contrib.django.models import sentry_exception_handler


class BusinessException(Exception):
    pass


class NoAvailableSeatsError(BusinessException):
    pass


class AlreadyJoinedError(BusinessException):
    pass


class NoRightException(BusinessException):

    def __init__(self, message=u"对不起，您没有权限执行此操作！"):
        self.message = message


class AliapyBackVerifyFailedError(BusinessException):
    def __init__(self, message=u"对不起，出错了，请您查看订单是否支付成功！"):
        self.message = message


#担保交易换成及时支付后，会设置支付有效时间，不会出现这种异常
class PayOverTimeError(BusinessException):
    def __init__(self, message=u"对不起，您支付已经超时，请联系饭聚网退款！"):
        self.message = message

alipay_wap_sync_back = reverse_lazy("alipay_wap_sync_back")


class ProcessExceptionMiddleware(object):
    def process_exception(self, request, exception):
        if not settings.DEBUG:
            sentry_exception_handler(request=request)
            if request.path != alipay_wap_sync_back:
                return TemplateResponse(request, "500.html", {'exception': exception})
            else:
                return HttpResponseRedirect("%s?message=%s" % (reverse_lazy('error'), exception.message))
        else:
            return None
