#coding=utf-8
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils import simplejson
from taggit.models import Tag
from eo.models import UserProfile

SUCESS = "OK"
ERROR = 'NOK'


# Create a json response with status and message)
def create_json_response(status=None, message=None, extra_dict=None):
    response = {}
    if status:
        response['status'] = status
    if message:
        response['message'] = message
    if extra_dict:
        response.update(extra_dict)
    return HttpResponse(simplejson.dumps(response), content_type='application/json', )


def create_sucess_json_response(message=u"成功", extra_dict=None):
    return create_json_response(SUCESS, message, extra_dict)


def create_failure_json_response(message=u"操作失败", extra_dict=None):
    return create_json_response(ERROR, message, extra_dict)


def create_no_right_response(message=u'对不起，您没有权限执行此操作'):
    return create_json_response(ERROR, message)


def list_tags(request):
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    if query:
        tag_name_qs = Tag.objects.filter(name__icontains=query).values_list('name')
    else:
        tag_name_qs = UserProfile.tags.most_common().values_list('name','num_times' )
        if len(tag_name_qs) < 10:
            tag_name_qs=[(u'读书',),(u'运动',),(u'K歌',),(u'登山',),(u'骑行',),(u'公益',)]

    paginator = Paginator(tag_name_qs, 10)
    if paginator.num_pages >= page:
        data = [{'value': tag[0]} for tag in paginator.page(page).object_list]
    else:
        data = []
    return HttpResponse(simplejson.dumps(data), content_type='application/json', )

