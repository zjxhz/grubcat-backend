#-*- coding:utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.conf import settings as django_settings


class settings:
    # 安全检验码，以数字和字母组成的32位字符
    MD5_KEY = '7g5w00e0eu37l8tm85pp1wutcoxjglzl'
    ALIPAY_PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCFUVMaKGT8icZzzEtHi96jBpUI
WQuhELISCor9m9wJZ78HanKBX+t1cNYy0G+9trYJC3nZUgH3PF/evHsnABlvKrgY
vttFLoHk/5GEBaG4h3o18NBP2YDktzUfzKUhwJhwKJDTxZv4u462m38bFgDij4Px
KiT3hR3chcuQnwMi5wIDAQAB
-----END PUBLIC KEY-----'''
    FANJOIN_PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDjL15OEbKYVDK+jJNpxL3ejLxD
IcnUet2Up9Z9HOHMTOcF4asAD1a/6Is7KabVoOEr4ycMAn2K4Sy6ONVtJF/3lq4a
+yqQAVpcSevFXb3puiIeHpAaMhMeLJ5YMSxVoGTtz3QQELao2p2M30NlHK42jlGq
9LQ844IfUEbL68YLkQIDAQAB
-----END PUBLIC KEY-----'''
    FANJOIN_PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDjL15OEbKYVDK+jJNpxL3ejLxDIcnUet2Up9Z9HOHMTOcF4asA
D1a/6Is7KabVoOEr4ycMAn2K4Sy6ONVtJF/3lq4a+yqQAVpcSevFXb3puiIeHpAa
MhMeLJ5YMSxVoGTtz3QQELao2p2M30NlHK42jlGq9LQ844IfUEbL68YLkQIDAQAB
AoGAR+mxl1LAzrkwSuLissNFOtIfsbxbT/gIdcre+UGQNARPyKvTXjR8yEiK8hJQ
LiU7wZGoxYNwS+rVJqlg3ah6+6K07YQlWhROStveRoI5LMrUGQ10/ng+Fe5enuW6
tDAkkaVD89zuoB74dJnt8CUHNHumPlTGaR+0V0rCvl1jJ1UCQQD0bX6TH5rCrjwg
/zRLvQNP3TOYQtoU7Ev77rCnhz50lPftVN00DHzEfosY9ZAqbyUZL7l+XRfmiqLT
WPT260/DAkEA7fDjxQQ0fkHpEhfD988U/MmG1Sflrlp2kevMQhaZCudZFtUUw+2/
RkDsZXzPfgVYoEDIK9t+5fiSgHuN7MC2GwJBAIhB+cueVLGuW4qxeb+28H+2+iop
KlV7nKgm2YeqlyB6YvOE2YNIas1HFdemHOXq661ss2VEFCzKoBZdgsGbT+0CQQDC
CSN1UsyL+avbeU3yFAmFa8JsqTCAUn1G2gekDVGYtrjMCc/5RzQoUmF1EacTmcCA
TtPuD/0YBPFTnW5Ll4vpAkBQOHNC/qht85wquf9YEBU7XTs450AhS9Unt6SOEIM5
Gja3UhMgqiy8b+H9BrRtjlNsS/txhhCEkSm8UbYFSCyK
-----END RSA PRIVATE KEY-----'''
    ALIPAY_INPUT_CHARSET = 'utf-8'
    # 合作身份者ID，以2088开头的16位纯数字
    ALIPAY_PARTNER = '2088901270565065'

    # 签约支付宝账号或卖家支付宝帐户
    ALIPAY_SELLER_EMAIL = 'fanjoin.com@gmail.com'

    ALIPAY_DIRECT_SIGN_TYPE = 'MD5'
    ALIPAY_APP_SIGN_TYPE = 'RSA'

    # 付完款后跳转的页面（web同步通知,web异步通知,wap同步通知,wap异步通知） 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
    ALIPAY_DIRECT_SYNC_BACK_URL = '%s%s' % (django_settings.ALIPAY_BACK_DOMAIN, 'pay/alipay/direct/back/sync/')
    ALIPAY_DIRECT_ASYNC_BACK_URL = '%s%s' % (django_settings.ALIPAY_BACK_DOMAIN, 'pay/alipay/direct/back/async/')
    ALIPAY_APP_SYNC_BACK_URL = '%s%s' % (django_settings.ALIPAY_BACK_DOMAIN, 'pay/alipay/app/back/sync/')
    ALIPAY_APP_AYSNC_BACK_URL = '%s%s' % (django_settings.ALIPAY_BACK_DOMAIN, 'pay/alipay/app/back/async/')
    ALIPAY_WAP_SYNC_BACK_URL = '%s%s' % (django_settings.ALIPAY_BACK_DOMAIN, 'pay/alipay/wap/back/sync/')
    ALIPAY_WAP_AYSNC_BACK_URL = '%s%s' % (django_settings.ALIPAY_BACK_DOMAIN, 'pay/alipay/wap/back/async/')

    # 访问模式,根据自己的服务器是否支持ssl访问，若支持请选择https；若不支持请选择http
    ALIPAY_TRANSPORT = 'http'
