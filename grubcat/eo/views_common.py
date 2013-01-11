#coding=utf-8
from django.core.paginator import Paginator
from django.http import HttpResponse
import simplejson
from taggit.models import Tag
from eo.models import UserProfile

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
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')