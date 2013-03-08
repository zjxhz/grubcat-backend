from django.conf import settings
from xmpp.protocol import NS_DATA
import json
import logging
import pyapns
import socket
import xmpp

logger = logging.getLogger("api")

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

    
def get_xmpp_username_and_password(user_profile):
    if user_profile.weibo_access_token:
        password = user_profile.weibo_access_token
    else:
        password = user_profile.user.password
    return escape_xmpp_node(user_profile.user.username), password

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

class XMPPClientWrapper(object):
    PORT = 5055
    def syncName(self, user_profile):
        logger.debug("sync name of %s " % user_profile)
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(('localhost',self.PORT)) 
        dic = {'task':"syncname", 'username':escape_xmpp_node(user_profile.user.username), "password":user_profile.user.password, "name": user_profile.name}
        soc.send(json.dumps(dic))
        logger.debug("sync name finished with response: %s " % soc.recv(1024))
    
    def syncAvatar(self, user_profile):
        logger.debug("sync avatar of %s " % user_profile)
        dic = {'task':"syncavatar",'username':escape_xmpp_node(user_profile.user.username), "password":user_profile.user.password, "avatar": user_profile.small_avatar_path}
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(('localhost',self.PORT)) 
        soc.send(json.dumps(dic))
        logger.debug("sync avatar finished with response: %s " % soc.recv(1024))
        
    def syncProfile(self, user_profile):
        logger.debug("sync avatar of %s " % user_profile)
        if user_profile.weibo_access_token:
            password = user_profile.weibo_access_token
        else:
            password = user_profile.user.password
        dic = {'task':"syncprofile",'username':escape_xmpp_node(user_profile.user.username), "password":password, "name": user_profile.name, "avatar": user_profile.small_avatar_path}
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(('localhost',self.PORT)) 
        soc.send(json.dumps(dic))
        logger.debug("sync profile finished with response: %s " % soc.recv(1024))
        soc.close()

class PubSub(object):
    def createNode(self, user_profile, node_name):
        username, pw =get_xmpp_username_and_password(user_profile) 
#        username, pw =settings.XMPP_PUBSUB_USER, settings.XMPP_PUBSUB_PASSWORD
        jid = xmpp.protocol.JID(username + "@fanjoin.com")
        logger.debug("%s is creating node: %s" % (username, node_name))
        
        cl=xmpp.Client(settings.XMPP_SERVER,debug=settings.XMPP_DEBUG)
        cl.connect()
        cl.auth(str(jid), pw)
        
        iq = self.buildIq()
        iq.T.pubsub.NT.create['node']=node_name
#        enable below lines if needed
#        x_node = iq.NT.configure.NT.x
#        x_node["xmlns"]=NS_DATA
#        field = x_node.NT.field
#        field["var"]="pubsub#send_last_published_item"
#        field.NT.value="never"
        
        cl.send(iq)
        cl.Process(1)
        cl.disconnect()
        
    def subscribe(self, subscriber, node_name, subscribing=True):
        username, pw =get_xmpp_username_and_password(subscriber)
        jid = xmpp.protocol.JID(username + "@fanjoin.com")
        
        logger.debug("%s is subscribing(%s) node: %s" % (username, subscribing, node_name))
        
        cl=xmpp.Client(settings.XMPP_SERVER,debug=settings.XMPP_DEBUG)
        cl.connect()
        cl.auth(str(jid), pw)
        
        iq = self.buildIq()
        if subscribing:
            subscribe_node = iq.T.pubsub.NT.subscribe
        else:
            subscribe_node = iq.T.pubsub.NT.unsubscribe
        subscribe_node['node']=node_name
        subscribe_node['jid']=str(jid)
        cl.send(iq)
        cl.Process(1)
        cl.disconnect()
        
    def unsubscribe(self, subscriber, node_name):
        self.subscribe(subscriber, node_name, False)

    def publish(self, publisher, node_name, payload):
        username, pw =get_xmpp_username_and_password(publisher)
#        username, pw =settings.XMPP_PUBSUB_USER, settings.XMPP_PUBSUB_PASSWORD
        jid = xmpp.protocol.JID(username + "@fanjoin.com")
        
        logger.debug("%s is publishing node: %s with payload: %s" % (username, node_name, payload))
        
        cl=xmpp.Client(settings.XMPP_SERVER,debug=settings.XMPP_DEBUG)
        cl.connect()
        cl.auth(str(jid), pw)
        
        iq = self.buildIq()
        iq.T.pubsub.NT.publish['node'] = node_name
        iq.T.pubsub.T.publish.T.item = ""
        iq.T.pubsub.T.publish.T.item.T.entry = payload
        iq.T.pubsub.T.publish.T.item.T.entry.namespace = 'http://www.w3.org/2005/Atom'
        cl.send(iq)
        cl.Process(1)
        cl.disconnect()
        
    def buildIq(self):
        iq = xmpp.protocol.Iq('set', to = settings.XMPP_PUBSUB_SERVICE)
        iq.NT.pubsub['xmlns']=xmpp.protocol.NS_PUBSUB
        return iq
pubsub = PubSub()        