#coding=utf-8
from django.conf import settings
from django.template.response import TemplateResponse
from raven.contrib.django.models import sentry_exception_handler


class BusinessException(Exception):
    message = u"对不起，您的操作有误！"


class NoAvailableSeatsError(BusinessException):
    message = u"对不起，饭局人数已满，您可以加入其他感兴趣的饭局！"


class AlreadyJoinedError(BusinessException):
    message = u"对不起，您已经加入了这个饭局，您可以加入其他感兴趣的饭局！"


class NoRightException(BusinessException):
    message = u"对不起，您没有权限执行此操作！"


class AliapyBackVerifyFailedError(BusinessException):
    message = u"对不起，出错了，请您查看订单是否支付成功！"


#担保交易换成及时支付后，会设置支付有效时间，不会出现这种异常
class PayOverTimeError(BusinessException):
    message = u'对不起，您支付已经超时，请联系饭聚网退款！'


class ProcessExceptionMiddleware(object):
    def process_exception(self, request, exception):
        if not settings.DEBUG:
            sentry_exception_handler(request=request)
            return TemplateResponse(request, "500.html", {'exception': exception})
