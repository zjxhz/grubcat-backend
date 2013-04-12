# -*- coding: utf-8 -*-
'''
Created on 2011-4-21
支付宝接口
@author: Yefe
'''
from base64 import b64decode
import base64
import logging
import xml.dom.minidom
from urllib import urlencode, urlopen, unquote_plus, quote_plus
import M2Crypto
from rsa._compat import b
from django.utils.encoding import smart_str
import rsa
from werkzeug.urls import url_decode
from eo.exceptions import AliapyBackVerifyFailedError
from hashcompat import md5_constructor as md5
from config import settings
from django.conf import settings as django_settings

pay_logger = logging.getLogger("pay")
order_prefix = getattr(django_settings, 'ORDER_PREFIX', '')
# 网关地址
_WEB_GATEWAY = 'https://www.alipay.com/cooperate/gateway.do?'
_APP_GATEWAY = "http://wappaygw.alipay.com/service/rest.htm?"


def decrypt(data):
    private_key = M2Crypto.RSA.load_key_string(open("D:/soft/alipay/bin/rsa_private_key.pem", "rb").read())
    content = base64.decodestring(data)
    i = 0
    length = len(content) / 128
    result = ''
    while i < length:
        d = content[i * 128:(i + 1) * 128]
        result += private_key.private_decrypt(d, M2Crypto.RSA.pkcs1_padding)
        i += 1
    return result


def build_mysign(data, sign_type='RSA'):
# 生成签名结果
    if sign_type == 'MD5':
        return md5(data + settings.MD5_KEY).hexdigest()
    elif sign_type == 'RSA':
        private_key_str = M2Crypto.RSA.load_key_string(open("D:/soft/alipay/bin/rsa_private_key.pem", "rb").read())
        m = M2Crypto.EVP.MessageDigest('sha1')
        m.update(data)
        digest = m.final()
        sign = private_key_str.sign(digest, "sha1")
        return sign
    return ''


def verify_sign(data, sort=None):
    # 初级验证--签名
    _, msg = params_filter(data, sort)
    try:
        key = M2Crypto.RSA.load_pub_key_bio(M2Crypto.BIO.MemoryBuffer(open("D:/soft/alipay/bin/alipay_rsa_public_key.pem","rb").read()))
        m = M2Crypto.EVP.MessageDigest('sha1')
        m.update(msg)
        digest = m.final()
        result = key.verify(digest, base64.decodestring(data.get('sign')), "sha1")
        if not result:
            pay_logger.error("支付宝返回校验失败")
            raise AliapyBackVerifyFailedError
    except Exception, e:
        pay_logger.error("支付宝返回校验失败" + str(e))
        raise AliapyBackVerifyFailedError
        # mysign = build_mysign(prestr, settings.ALIPAY_PRIVATE_KEY, settings.ALIPAY_WAP_SIGN_TYPE)
        # if mysign != data.get('sign'):
        #     pay_logger.error("支付宝返回校验失败，mysign: %s alisign: %s" % (mysign, data.get('sign')))
        #     raise AliapyBackVerifyFailedError


def params_filter(params, sort=None, template='%s=%s&'):
# 对数组排序并除去数组中的空值和签名参数
# 返回数组和链接串
    newparams = {}
    prestr = ''
    if not sort:
        ks = params.keys()
        ks.sort()
    else:
        ks = sort

    for k in ks:
        v = params[k]
        k = smart_str(k, settings.ALIPAY_INPUT_CHARSET)
        if k not in ('sign', 'sign_type') and v != '':
            newparams[k] = smart_str(v, settings.ALIPAY_INPUT_CHARSET)
            prestr += template % (k, newparams[k])
    prestr = prestr[:-1]
    return newparams, prestr


def create_direct_pay(order, subject, body, price, quantity=""):
    # 即时到账交易接口
    params = {}
    params['service'] = 'create_direct_pay_by_user'
    params['payment_type'] = '1'

    # 获取配置文件
    params['partner'] = settings.ALIPAY_PARTNER
    params['seller_id'] = settings.ALIPAY_PARTNER
    params['return_url'] = settings.ALIPAY_DIRECT_SYNC_BACK_URL
    params['notify_url'] = settings.ALIPAY_DIRECT_ASYNC_BACK_URL
    params['_input_charset'] = settings.ALIPAY_INPUT_CHARSET

    # 从订单数据中动态获取到的必填参数
    params['out_trade_no'] = order_prefix + str(order)        # 请与贵网站订单系统中的唯一订单号匹配
    params['subject'] = subject   # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
    params['body'] = body      # 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里
    # TODO 超时设置
    # params['it_b_pay'] = str(django_settings.PAY_OVERTIME) + 'm'
    params['price'] = 0.01 #TODO price             # 单价
    params['quantity'] = quantity       # 商品的数量
    # 扩展功能参数——网银提前

    params, prestr = params_filter(params)

    params['sign'] = build_mysign(prestr, settings.ALIPAY_SIGN_TYPE)
    params['sign_type'] = settings.ALIPAY_SIGN_TYPE

    return _WEB_GATEWAY + urlencode(params)

def create_app_pay(order, subject, body, total_fee):
    # app安全支付接口
    params = {}
    # 获取配置文件
    params['partner'] = settings.ALIPAY_PARTNER
    params['seller'] = settings.ALIPAY_PARTNER
    params['notify_url'] = settings.ALIPAY_APP_SYNC_BACK_URL

    # 从订单数据中动态获取到的必填参数
    params['out_trade_no'] = order_prefix + str(order)  # 贵网站订单系统中的唯一订单号匹配
    params['subject'] = subject   # 订单名称
    params['body'] = body
    # TODO 超时设置 app支付没有这个参数
    # params['it_b_pay'] = str(django_settings.PAY_OVERTIME) + 'm'
    params['total_fee'] = 0.01 #TODO

    params, req_str = params_filter(params, template='%s="%s"&')
    sign = base64.encodestring(build_mysign(req_str))
    return '%s&sign="%s"&sign_type="%s"' % ( req_str, sign, settings.ALIPAY_APP_SIGN_TYPE)


