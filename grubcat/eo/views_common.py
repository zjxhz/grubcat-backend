#coding=utf-8
from datetime import datetime, timedelta
import logging
import urllib
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse
from taggit.models import Tag
import time
from eo.exceptions import *
from eo.models import UserProfile, Order, OrderStatus, TransFlow
from eo.pay.alipay.alipay import send_goods_confirm_by_platform, notify_verify
import json

SUCESS = "OK"
ERROR = 'NOK'
pay_logger = logging.getLogger("pay")
order_prefix = getattr(settings, 'ORDER_PREFIX', '')

def handle_alipay_back(data):
    """
        handle both sync and async notifier
        @exception:　AliapyBackVerifyFailedError 支付宝返回数据校验失败，此种情况一般不会有
        @exception:  PayOverTimeError 支付超时，替换成及时支付后，不会出现这种情况
        @exception: AlreadyJoinedError 重复支付
    """
    pay_logger.info(data)
    trade_status = data.get('trade_status')
    if trade_status == 'WAIT_SELLER_SEND_GOODS':
        order = Order.objects.get(pk=data.get('out_trade_no').replace(order_prefix, ''))
        alipay_trade_no = data.get('trade_no')
        try:
            payed_time = time.strptime(data.get('gmt_payment'), '%Y-%m-%d %H:%M:%S')
            payed_time = datetime(*payed_time[:6])
        except:
            payed_time = datetime.now()

        if hasattr(order, 'flow'):
            #already handled before
            if order.created_time + timedelta(minutes=settings.PAY_OVERTIME) < payed_time:
                #pay overtime and handled before
                raise PayOverTimeError
            elif order.status == OrderStatus.PAYIED:
                return
            elif order.status == OrderStatus.CANCELED:
                #another order paied and this order is  handled before
                raise AlreadyJoinedError(u'对不起，您重复支付了，请您联系我们退款！')

        #fist time handled back request from alipay
        if not notify_verify(data):
            pay_logger.error(u"alipay返回, 校验失败")
            raise AliapyBackVerifyFailedError

        #TODO remove overtime check
        if order.created_time + timedelta(minutes=settings.PAY_OVERTIME) < payed_time:
            order.status = OrderStatus.CANCELED
            order.payed_time = payed_time
            order.save()
            TransFlow.objects.create(order=order, alipay_trade_no=alipay_trade_no)
            raise PayOverTimeError

        elif order.status == OrderStatus.CREATED:
            order.set_payed(payed_time)
            TransFlow.objects.create(order=order, alipay_trade_no=alipay_trade_no)
            url = send_goods_confirm_by_platform(alipay_trade_no)
            urllib.urlopen(url)
            pay_logger.info('确认发货.订单:%s, url:%s' % (order.id, url))

        elif order.status == OrderStatus.CANCELED:
            #another order paied and this order is not handled before
            order.payed_time = payed_time
            order.save()
            TransFlow.objects.create(order=order, alipay_trade_no=alipay_trade_no)
            raise AlreadyJoinedError(u'对不起，您重复支付了，请您联系我们退款！')

    else:
        pay_logger.debug(u"alipay返回状态不是WAIT_SELLER_SEND_GOODS，是%s" % trade_status)


# Create a json response with status and message)
def create_json_response(status=None, message=None, extra_dict=None):
    response = {}
    if status:
        response['status'] = status
    if message:
        response['message'] = message
    if extra_dict:
        response.update(extra_dict)
    return HttpResponse(json.dumps(response), content_type='application/json', )


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