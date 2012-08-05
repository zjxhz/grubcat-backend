#coding=utf-8
from django.conf import settings
from django.template.response import TemplateResponse
from django.views.generic.simple import direct_to_template

class BusinessException(Exception):
    message = u"对不起，您的操作有误！"

class NoAvailableSeatsError(BusinessException):
    message = u"对不起，饭局人数已满，您可以加入其他感兴趣的饭局！"

class AlreadyJoinedError(BusinessException):
    message = u"对不起，您已经加入了这个饭局，您可以加入其他感兴趣的饭局！"

class ProcessExceptionMiddleware(object):
    def process_exception(self, request, exception):
        if not settings.debug and (isinstance(exception, BusinessException) or not settings.SHOW_EXCEPTION_DETAIL):
            return TemplateResponse(request, "500.html", {'exception': exception})
