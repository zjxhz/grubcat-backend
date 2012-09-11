#coding=utf-8

from django.core import serializers
from django.http import HttpResponse
from django.utils import simplejson

def writeJson(qs, response, relations=None):
    json_serializer = serializers.get_serializer("json")()
    if relations:
        return json_serializer.serialize(qs, ensure_ascii=False, relations=relations, stream=response)
    return json_serializer.serialize(qs, ensure_ascii=False, stream=response)


def getJsonResponse(qs, relations=None):
    response = HttpResponse(content_type='application/json')
    writeJson(qs, response, relations)
    return response

SUCESS = "OK"
ERROR = 'NOK'

# Create a general response with status and message)
def createGeneralResponse(status, message, extra_dict=None):
    response = {'status': status, 'info': message}
    if extra_dict:
        response.update(extra_dict)
    return HttpResponse(simplejson.dumps(response))

# Create a general response with status and message)
def creatJsonResponse(status, message, extra_dict=None):
    response = {'status': status, 'message': message}
    if extra_dict:
        response.update(extra_dict)
    return HttpResponse(simplejson.dumps(response), content_type='application/json', )

# Create a general response with status and message)
# Create a general response with status and message)

def createSucessJsonResponse(message=u"成功", extra_dict=None):
    return creatJsonResponse(SUCESS, message, extra_dict)
def createFailureJsonResponse(message=u"操作失败", extra_dict=None):
    return creatJsonResponse(ERROR, message, extra_dict)

def create_no_right_response():
    return creatJsonResponse(ERROR, u'对不起，您没有权限执行此操作')