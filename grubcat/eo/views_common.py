#coding=utf-8
from datetime import datetime, timedelta
import logging
import threading
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse
from taggit.models import Tag
import time
from eo.exceptions import *
from eo.models import UserProfile, Order, OrderStatus, TransFlow
import json

SUCESS = "OK"
ERROR = 'NOK'
pay_logger = logging.getLogger("pay")
order_prefix = getattr(settings, 'ORDER_PREFIX', '')


alipay_lock = threading.Lock()


def handle_alipay_back(order_id, alipay_trade_no='', payed_time_str='', check_overtime=False):
    """
        handle both sync and async notifier
        @exception:　AliapyBackVerifyFailedError 支付宝返回数据校验失败，此种情况一般不会有
        @exception: AlreadyJoinedError 重复支付
    """
    if payed_time_str:
        try:
            payed_time = time.strptime(payed_time_str, '%Y-%m-%d %H:%M:%S')
            payed_time = datetime(*payed_time[:6])
        except:
            payed_time = datetime.now()
    else:
        payed_time = datetime.now()

    try:
        if alipay_lock.acquire():
            order = Order.objects.get(pk=order_id)

            if payed_time and not order.payed_time:
                order.payed_time = payed_time
                order.save()

            if alipay_trade_no and not hasattr(order, 'flow'):
                TransFlow.objects.create(order=order, alipay_trade_no=alipay_trade_no)

            if check_overtime and order.created_time + timedelta(
                    minutes=settings.PAY_OVERTIME) < payed_time:
                try:
                    order.meal.checkAvaliableSeats(order.customer, order.num_persons)
                except NoAvailableSeatsError:
                    raise PayOverTimeError(u'对不起，您支付超时了，请您联系饭聚网客服!')

            if order.status == OrderStatus.CREATED:
                order.set_payed()
            elif order.status == OrderStatus.CANCELED:
                #another order paied and this order is not handled before
                raise AlreadyJoinedError(u'对不起，您重复支付了，请您联系我们退款！')

    finally:
        alipay_lock.release()


# Create a json response with status and message)
def create_json_response(status=None, message=None, extra_dict=None):
    response = {}
    if status:
        response['status'] = status
    if message:
        response['message'] = message
    if extra_dict:
        response.update(extra_dict)
    return HttpResponse(json.dumps(response), content_type='application/json;charset=UTF-8', )


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
        tag_name_qs = UserProfile.tags.most_common().values_list('name', 'num_times')
        if len(tag_name_qs) < 10:
            tag_name_qs = [(u'读书',), (u'运动',), (u'K歌',), (u'登山',), (u'骑行',), (u'公益',)]

    paginator = Paginator(tag_name_qs, 10)
    if paginator.num_pages >= page:
        data = [{'value': tag[0]} for tag in paginator.page(page).object_list]
    else:
        data = []
    return HttpResponse(json.dumps(data), content_type='application/json', )


def add_tag(request):
    if request.method == 'POST':
        tag = request.POST.get('tag')
        request.user.get_profile().tags.add(tag)
        return create_sucess_json_response()