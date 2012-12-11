import pyapns
import socket
import json 
import logging

logger = logging.getLogger("api")

class PyapnsWrapper(object):
 
    def __init__(self, host, app_id, apns_certificate_file, mode='sandbox'):
        self.app_id = app_id
        pyapns.configure({'HOST': host})
        pyapns.provision(app_id,
                         open(apns_certificate_file).read(),
                         mode)
 
    def notify(self, token, message):
        pyapns.notify(self.app_id,token,{'aps':{'alert': message}})

class XMPPClientWrapper(object):
    PORT = 5055
   
    def escape_node(self, node):
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
    
    def syncName(self, user_profile):
        logger.debug("sync name of %s " % user_profile)
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(('localhost',self.PORT)) 
        dic = {'task':"syncname", 'username':self.escape_node(user_profile.user.username), "password":user_profile.user.password, "name": user_profile.name}
        soc.send(json.dumps(dic))
        logger.debug("sync name finished with response: %s " % soc.recv(1024))
    
    def syncAvatar(self, user_profile):
        logger.debug("sync avatar of %s " % user_profile)
        dic = {'task':"syncavatar",'username':self.escape_node(user_profile.user.username), "password":user_profile.user.password, "avatar": user_profile.small_avatar_path}
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(('localhost',self.PORT)) 
        soc.send(json.dumps(dic))
        logger.debug("sync avatar finished with response: %s " % soc.recv(1024))