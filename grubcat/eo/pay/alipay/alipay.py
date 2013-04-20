# -*- coding: utf-8 -*-
import base64
import logging
import xml.dom.minidom
from urllib import urlencode, quote_plus, urlopen, unquote_plus

import M2Crypto
from M2Crypto import BIO
from django.utils.encoding import smart_str
from django.conf import settings as django_settings

from eo.exceptions import AliapyBackVerifyFailedError
from hashcompat import md5_constructor as md5
from config import settings


pay_logger = logging.getLogger("pay")
order_prefix = getattr(django_settings, 'ORDER_PREFIX', '')
# 网关地址
_WEB_GATEWAY = 'https://www.alipay.com/cooperate/gateway.do?'
_WAP_GATEWAY = "http://wappaygw.alipay.com/service/rest.htm?"


def create_wap_pay(order, subject, price, quantity):
    params = {'service': 'alipay.wap.trade.create.direct',
              'format': 'xml', 'v': '2.0',
              'partner': settings.ALIPAY_PARTNER,
              'req_id': order_prefix + str(order),
              'pay_expire': django_settings.PAY_OVERTIME_FOR_PAY_OR_USER,
              'sec_id': '0001'}

    #req data
    req_data = {'subject': subject,
                'out_trade_no': order_prefix + str(order),
                'total_fee': str(price * quantity),
                'seller_account_name': settings.ALIPAY_SELLER_EMAIL,
                'call_back_url': settings.ALIPAY_WAP_SYNC_BACK_URL,
                'notify_url': settings.ALIPAY_WAP_AYSNC_BACK_URL,
                'pay_expire': django_settings.PAY_OVERTIME}
    #build req_data
    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, 'direct_trade_create_req', None)
    root = dom.documentElement
    req_data,_ = params_filter(req_data)
    for k in req_data:
        item = dom.createElement(k)
        text = dom.createTextNode(str(req_data[k]))
        item.appendChild(text)
        root.appendChild(item)
    params['req_data'] = root.toxml()
    new_params, prestr = params_filter(params)

    params['sign'] = build_mysign(prestr)
    auth_result = urlopen(_WAP_GATEWAY + urlencode(params)).read()
    auth_result = unquote_plus(auth_result).split("&")
    auth_result_param = {}
    for p in auth_result:
        index = p.index('=')
        auth_result_param[p[:index]] = p[index+1:]
    if 'res_error' in auth_result_param:
        print auth_result_param.get('res_error')
        #TODO
        raise
    auth_result_param['res_data'] = decrypt(auth_result_param['res_data'])
    verify_sign(auth_result_param)

    doc = xml.dom.minidom.parseString(auth_result_param['res_data'])
    request_token = doc.getElementsByTagName("request_token")[0].firstChild.data

    params['service'] = 'alipay.wap.auth.authAndExecute'

    #req data
    req_data = {'request_token': request_token}
    #build req_data
    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, 'auth_and_execute_req', None)
    root = dom.documentElement
    req_data, _ = params_filter(req_data)
    for k in req_data:
        item = dom.createElement(k)
        text = dom.createTextNode(str(req_data[k]))
        item.appendChild(text)
        root.appendChild(item)
    params['req_data'] = root.toxml()
    params, prestr = params_filter(params)

    params['sign'] = build_mysign(prestr)
    return _WAP_GATEWAY + urlencode(params)


def create_direct_pay(order, subject, price, quantity=""):
    # 即时到账交易接口
    params = {'service': 'create_direct_pay_by_user',
              'payment_type': '1',
              'partner': settings.ALIPAY_PARTNER,
              'seller_id': settings.ALIPAY_PARTNER,
              'return_url': settings.ALIPAY_DIRECT_SYNC_BACK_URL,
              'notify_url': settings.ALIPAY_DIRECT_ASYNC_BACK_URL,
              '_input_charset': settings.ALIPAY_INPUT_CHARSET,
              'out_trade_no': order_prefix + str(order),
              'subject': (u'饭局： %s' % subject),
              'body': subject,
              'price': 0.01,
              'quantity': quantity,
              'it_b_pay': str(django_settings.PAY_OVERTIME_FOR_PAY_OR_USER) + 'm'}

    params, prestr = params_filter(params)

    params['sign'] = build_mysign(prestr, settings.ALIPAY_DIRECT_SIGN_TYPE)
    params['sign_type'] = settings.ALIPAY_DIRECT_SIGN_TYPE

    return _WEB_GATEWAY + urlencode(params)


def create_app_pay(order, subject, total_fee):
    # app安全支付接口
    params = {'partner': settings.ALIPAY_PARTNER,
              'seller': settings.ALIPAY_PARTNER,
              'notify_url': settings.ALIPAY_APP_AYSNC_BACK_URL,
              'out_trade_no': order_prefix + str(order),
              'subject': u'饭局：%s' % subject,
              'body': subject,
              'total_fee': 0.01}

    params, req_str = params_filter(params, template='%s="%s"&')
    sign = build_mysign(req_str)
    return '%s&sign="%s"&sign_type="%s"' % (req_str, quote_plus(sign), settings.ALIPAY_APP_SIGN_TYPE)


def build_mysign(data, sign_type='RSA'):
# 生成签名结果
    if sign_type == 'MD5':
        return md5(data + settings.MD5_KEY).hexdigest()
    elif sign_type == 'RSA':
        private_key_str = M2Crypto.RSA.load_key_string(settings.FANJOIN_PRIVATE_KEY)
        m = M2Crypto.EVP.MessageDigest('sha1')
        m.update(data)
        digest = m.final()
        sign = private_key_str.sign(digest, "sha1")
        return base64.b64encode(sign)
    return ''


def verify_sign(data, sign='', signType='RSA', sort=None):
    # 初级验证--签名
    if hasattr(data, "items"):
        _, msg = params_filter(data, sort)
    else:
        msg = smart_str(data)
    if not sign:
        sign = data.get('sign')

    result = False
    if signType == 'RSA':
        public_key = M2Crypto.RSA.load_pub_key_bio(BIO.MemoryBuffer(settings.ALIPAY_PUBLIC_KEY))
        m = M2Crypto.EVP.MessageDigest('sha1')
        m.update(msg)
        digest = m.final()
        result = public_key.verify(digest, base64.b64decode(sign))
    elif signType == 'MD5':
        mysign = build_mysign(msg, 'MD5')
        result = mysign == sign

    if not result:
        raise AliapyBackVerifyFailedError


def decrypt(data):
    private_key = M2Crypto.RSA.load_key_string(settings.FANJOIN_PRIVATE_KEY)
    content = base64.b64decode(data)
    i = 0
    length = len(content) / 128
    result = ''
    while i < length:
        d = content[i * 128:(i + 1) * 128]
        result += private_key.private_decrypt(d, M2Crypto.RSA.pkcs1_padding)
        i += 1
    return result


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

