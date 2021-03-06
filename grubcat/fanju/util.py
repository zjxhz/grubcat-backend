from django.conf import settings
from django.contrib.gis.geoip import GeoIP
from django.db import connections
from settings import APNS_ENVIRONMENT
from xmpp.protocol import NS_DATA
import json
import logging
import pyapns
import socket
import xmpp

logger = logging.getLogger(__name__)

def escape_xmpp_node(node):
        node.strip()
        node = node.replace('\\', "\\5c")
        node = node.replace(' ',  "\\20")
        node = node.replace('\"', "\\22")
        node = node.replace('\&', "\\26")
        node = node.replace('\'', "\\27")
        node = node.replace('\/', "\\2f")
        node = node.replace(':',  "\\3a")
        node = node.replace('<',  "\\3c")
        node = node.replace('>',  "\\3e")
        node = node.replace('@',  "\\40")
        return node


def escape_xmpp_username(username):
    username = username.strip()
    username = username.replace("\\20", " ")
    username = username.replace("\\22", '"')
    username = username.replace("\\26", "&")
    username = username.replace("\\27", "'")
    username = username.replace("\\2f", "/")
    username = username.replace("\\3a", ":")
    username = username.replace("\\3c", "<")
    username = username.replace("\\3e", ">")
    username = username.replace("\\40", "@")
    username = username.replace("\\5c", "\\")  
    return username    

    
def get_xmpp_username_and_password(user=None):

    if not user:
        return 'pubsub', 'pubX3ae4+-'

    if user.weibo_access_token:
        password = user.weibo_access_token
    else:
        password = user.password
    return escape_xmpp_node(user.username), password


class PyapnsWrapper(object):
 
    def __init__(self, host, app_id, apns_certificate_file, mode=APNS_ENVIRONMENT):
        self.app_id = app_id
        pyapns.configure({'HOST': host})
        pyapns.provision(app_id,
                         open(apns_certificate_file).read(),
                         mode)
 
    def notify(self, token, message, badge=-1):
        dic = {'alert': message}
        if badge != -1:
            dic['badge'] = badge
        pyapns.notify(self.app_id,token,{'aps': dic})

# class XMPPClientWrapper(object):
#     PORT = 5055
#
#     def syncProfile(self, user_profile):
#         try:
#             logger.debug("sync avatar of %s " % user_profile)
#             if user_profile.weibo_access_token:
#                 password = user_profile.weibo_access_token
#             else:
#                 password = user_profile.password
#             dic = {'task':"syncprofile",'username':escape_xmpp_node(user_profile.username), "password":password, "name": user_profile.name, "avatar": user_profile.small_avatar_path}
#             soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             soc.connect(('localhost',self.PORT))
#             soc.send(json.dumps(dic))
#             logger.debug("sync profile finished with response: %s " % soc.recv(1024))
#             soc.close()
#         except Exception:
#             logger.error("failed to sync profile")

class PubSub(object):

    def create_client(self, user=None, client=None):
        username, pw = get_xmpp_username_and_password(user)
        jid = xmpp.protocol.JID("%s@%s" % (username, settings.CHATDOMAIN))
        if not client:
            client = xmpp.Client(settings.XMPP_SERVER, debug=settings.XMPP_DEBUG)
            client.connect(secure=0)
            client.auth(jid.getNode(), pw)
        return client, jid

    def create_node(self, node_name, client=None):
        try:

            cl, _ = self.create_client(client=client)
            logger.debug("creating node: %s" % node_name)

            iq = self.buildIq()
            iq.T.pubsub.NT.create['node']=node_name
    #        enable below lines if needed
    #        x_node = iq.NT.configure.NT.x
    #        x_node["xmlns"]=NS_DATA
    #        field = x_node.NT.field
    #        field["var"]="pubsub#send_last_published_item"
    #        field.NT.value="never"

            cl.send(iq)
            cl.Process(100)
            if not client:
                cl.disconnect()
        except Exception:
            logger.exception("xmpp error")

    def subscribe(self, subscriber, node_name, subscribing=True, client=None):
        try:
            cl, jid = self.create_client(subscriber, client)
            logger.debug("%s is subscribing(%s) node: %s" % (jid, subscribing, node_name))
            iq = self.buildIq()
            if subscribing:
                subscribe_node = iq.T.pubsub.NT.subscribe
            else:
                subscribe_node = iq.T.pubsub.NT.unsubscribe
            subscribe_node['node'] = node_name
            subscribe_node['jid'] = jid.getStripped()
            cl.send(iq)
            cl.Process(1)
            if not client:
                cl.disconnect()
        except Exception:
            logger.exception("xmpp error")
        
    def unsubscribe(self, subscriber, node_name, client=None):
        self.subscribe(subscriber, node_name, False, client=client)

    def publish(self, node_name, payload, client=None):
        try:

            cl, _ = self.create_client(client=client)
            logger.debug("publishing node: %s with payload: %s" % (node_name, payload))
            iq = self.buildIq()
            iq.T.pubsub.NT.publish['node'] = node_name
            iq.T.pubsub.T.publish.T.item = ""
            iq.T.pubsub.T.publish.T.item.T.entry = payload
            iq.T.pubsub.T.publish.T.item.T.entry.namespace = 'http://www.w3.org/2005/Atom'
            cl.send(iq)
            cl.Process(1)
            if not client:
                cl.disconnect()
        except Exception:
            logger.exception("xmpp error")

        
    def buildIq(self):
        iq = xmpp.protocol.Iq('set', to = settings.XMPP_PUBSUB_SERVICE)
        iq.NT.pubsub['xmlns']=xmpp.protocol.NS_PUBSUB
        return iq
pubsub = PubSub()


def common_context_processor(request):
    return {"CHATSERVER": settings.CHATSERVER, "CHATDOMAIN": settings.CHATDOMAIN}

# list of mobile User Agents
mobile_uas = [
    'w3c ', 'acs-', 'alav', 'alca', 'amoi', 'audi', 'avan', 'benq', 'bird', 'blac',
    'blaz', 'brew', 'cell', 'cldc', 'cmd-', 'dang', 'doco', 'eric', 'hipt', 'inno',
    'ipaq', 'java', 'jigs', 'kddi', 'keji', 'leno', 'lg-c', 'lg-d', 'lg-g', 'lge-',
    'maui', 'maxo', 'midp', 'mits', 'mmef', 'mobi', 'mot-', 'moto', 'mwbp', 'nec-',
    'newt', 'noki', 'oper', 'palm', 'pana', 'pant', 'phil', 'play', 'port', 'prox',
    'qwap', 'sage', 'sams', 'sany', 'sch-', 'sec-', 'send', 'seri', 'sgh-', 'shar',
    'sie-', 'siem', 'smal', 'smar', 'sony', 'sph-', 'symb', 't-mo', 'teli', 'tim-',
    'tosh', 'tsm-', 'upg1', 'upsi', 'vk-v', 'voda', 'wap-', 'wapa', 'wapi', 'wapp',
    'wapr', 'webc', 'winw', 'winw', 'xda', 'xda-'
]

mobile_ua_hints = ['SymbianOS', 'Opera Mini', 'iPhone']


def is_mobile_request(request):
    ''' Super simple device detection, returns True for mobile devices '''

    mobile_browser = False
    try:
        ua = request.META['HTTP_USER_AGENT'].lower()[0:4]

        if ua in mobile_uas:
            mobile_browser = True
        else:
            for hint in mobile_ua_hints:
                if request.META['HTTP_USER_AGENT'].find(hint) > 0:
                    mobile_browser = True
    except:
        pass

    return mobile_browser


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_location_by_ip(ip):
    try:
        geo_ip = GeoIP(cache=GeoIP.GEOIP_MEMORY_CACHE)
        return geo_ip.lat_lon(ip)
    except Exception:
        return None


def get_unread_message_count(user_name):
    user_name = "%s@%s" % (escape_xmpp_node(user_name).replace('\\', '\\\\'), settings.CHATDOMAIN)
    sql = "SELECT COUNT(*) FROM archiveMessages as m, archiveConversations as c  " \
          "WHERE m.conversationId=c.conversationId and  ((c.ownerJid='%s' and m.direction='from') or (c.withJid='%s' and m.direction='to')) and m.status=0 and m.type='chat'" % (
        user_name, user_name)
    cursor = connections['openfire'].cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    return row[0]

def get_unread_noty_count(user_name):
    user_name = "%s@%s" % (escape_xmpp_node(user_name).replace('\\', '\\\\'), settings.CHATDOMAIN)
    sql = "SELECT COUNT(*) FROM archiveMessages as m, archiveConversations as c  " \
          "WHERE m.conversationId=c.conversationId and  ((c.ownerJid='%s' and  c.withJid='%s') or (c.ownerJid='%s' and  c.withJid='%s')) and m.status=0" % (
        user_name, settings.XMPP_PUBSUB_SERVICE, settings.XMPP_PUBSUB_SERVICE,  user_name)
    cursor = connections['openfire'].cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    return row[0]