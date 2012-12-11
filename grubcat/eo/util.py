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
   
    
    def syncName(self, user_profile):
        logger.debug("sync name of %s " % user_profile)
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(('localhost',self.PORT)) 
        dic = {'task':"syncname", 'username':user_profile.user.username, "password":user_profile.user.password, "name": user_profile.name}
        soc.send(json.dumps(dic))
        logger.debug("sync name finished with response: %s " % soc.recv(1024))
    
    def syncAvatar(self, user_profile):
        logger.debug("sync avatar of %s " % user_profile)
        dic = {'task':"syncavatar",'username':user_profile.user.username, "password":user_profile.user.password, "avatar": user_profile.small_avatar_path}
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(('localhost',self.PORT)) 
        soc.send(json.dumps(dic))
        logger.debug("sync avatar finished with response: %s " % soc.recv(1024))