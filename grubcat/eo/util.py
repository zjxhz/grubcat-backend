import pyapns
import socket
import json 
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
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(('localhost',self.PORT))
        dic = {'username':user_profile.user.username, "password":user_profile.user.password, "name": user_profile.name}
        soc.send(json.dumps(dic))
    
    def syncAvatar(self, user_profile):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(('localhost',self.PORT))
        dic = {'username':user_profile.user.username, "password":user_profile.user.password, "avatar": user_profile.small_avatar_path}
        soc.send(json.dumps(dic))