from django.conf import settings
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

    
def get_xmpp_username_and_password(user):
    if user.weibo_access_token:
        password = user.weibo_access_token
    else:
        password = user.password
    return escape_xmpp_node(user.username), password

class PyapnsWrapper(object):
 
    def __init__(self, host, app_id, apns_certificate_file, mode='sandbox'):
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

    def create_client(self, subscriber, client=None):
        username, pw = get_xmpp_username_and_password(subscriber)
        jid = xmpp.protocol.JID("%s@%s" % (username, settings.CHATDOMAIN))
        if not client:
            client = xmpp.Client(jid.getDomain(), debug=settings.XMPP_DEBUG)
            client.connect(secure=0)
            client.auth(str(jid), pw)
        logger.debug('jid:%s' % str(jid))
        return client, jid

    def createNode(self, user, node_name, client=None):
        try:

            cl, jid = self.create_client(user, client)
            logger.debug("%s is creating node: %s" % (str(jid), node_name))

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
            logger.debug("%s is subscribing(%s) node: %s" % (str(jid), subscribing, node_name))
            iq = self.buildIq()
            if subscribing:
                subscribe_node = iq.T.pubsub.NT.subscribe
            else:
                subscribe_node = iq.T.pubsub.NT.unsubscribe
            subscribe_node['node']= node_name
            subscribe_node['jid']=str(jid)
            cl.send(iq)
            cl.Process(1)
            if not client:
                cl.disconnect()
        except Exception:
            logger.exception("xmpp error")
        
    def unsubscribe(self, subscriber, node_name, client=None):
        self.subscribe(subscriber, node_name, False, client=client)

    def publish(self, publisher, node_name, payload, client=None):
        try:

            cl, jid = self.create_client(publisher, client)
            logger.debug("%s is publishing node: %s with payload: %s" % (str(jid), node_name, payload))
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


def chat_context_processor(request):
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


def isMobileRequest(request):
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