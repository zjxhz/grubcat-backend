from twisted.internet import reactor
from twisted.words.protocols.jabber.jid import JID
from wokkel.client import XMPPClient
from wokkel.compat import IQ
from wokkel.subprotocols import XMPPHandler
from wokkel.xmppim import Presence
import hashlib
import logging
from django.conf import settings
from models import UserProfile

logger = logging.getLogger('api')

class AvatarUpdatedPresence(Presence):
    def __init__(self, sender, sha1):
        Presence.__init__(self)
        self['from']=sender
        x = self.addElement(('vcard-temp:x:update', 'x'))
        x.addElement('photo', content=sha1) 

NS_AVATAR='http://jabber.org/protocol/pubsub'
NS_VCARD_AVATAR='vcard-temp'
NS_ROSTER_ITEM='jabber:iq:roster'

class RosterClient(XMPPHandler):
    
    def __init__(self, jid, name):
        self.jid = jid
        self.name = name
        
    def addOrUpdateRosterItem(self):
        def processRosterResult(result):
            print result.toXml()
            
        iq = IQ(self.xmlstream, 'set')
        iq.addElement((NS_ROSTER_ITEM, 'query'))
        item = iq.query.addElement('item')
        item['jid'] = self.jid
        item['name'] = self.name
        item['subscription']='both'
        d = iq.send()
        d.addCallback(processRosterResult)
        return d
    
    def connectionInitialized(self):
        self.addOrUpdateRosterItem()
        
class AvatarClient(XMPPHandler):
    def __init__(self, jid, avatar):
        self.jid = jid
        self.avatar = avatar
        
    def connectionInitialized(self):
        self.publishvCardAvatar()

    def publishvCardAvatar(self):
        def processvCardAvatarUpdateResult(result):
            avatarUpdatedNotif = AvatarUpdatedPresence(self.jid, self.avatar_sha1)
            self.send(avatarUpdatedNotif)
            
        iq = IQ(self.xmlstream, 'set')
        iq['from']=self.jid
        vCard = iq.addElement((NS_VCARD_AVATAR, 'vCard'))
        photo = vCard.addElement('PHOTO')
        photo.addElement('TYPE', content='image/jpeg')
        content = open(self.avatar, "rb").read().encode("base64")
        self.avatar_sha1 = hashlib.sha1(content).digest()
        photo.addElement('BINVAL', content=content)
        d = iq.send()
        d.addCallback(processvCardAvatarUpdateResult)
        return d

def syncName(username, password, name):
    logger.debug("sync name of user '%s' to %s" % (username, name))
    jidStr = username + "@fanjoin.com"
    client = XMPPClient(JID(jidStr), password, settings.XMPP_SERVER) 
    roster = RosterClient(jidStr, name)
    roster.setHandlerParent(client)
    client.startService()

def syncAvatar(username, password, avatar):
    logger.debug("sync avatar of user '%s'" % username)
    jidStr = username + "@fanjoin.com"
    client = XMPPClient(JID(jidStr), password, settings.XMPP_SERVER) 
    avatar = AvatarClient(jidStr, avatar)
    avatar.setHandlerParent(client)
    client.startService()
  

def syncBoth(user_profile):
    syncName(user_profile.user.username, user_profile.user.password, user_profile.name)
    if user_profile.avatar:
        syncAvatar(user_profile.user.username, user_profile.user.password, user_profile.small_avatar_path)

reactor.run()    
#syncName("xuaxu","pbkdf2_sha256$10000$SOpptq1FcF8k$c8ttyX5qWC+bLlC71E2wPoFB54+oOz4wsleOKLptNBU=", "Wayne")
#syncAvatar("xuaxu","pbkdf2_sha256$10000$SOpptq1FcF8k$c8ttyX5qWC+bLlC71E2wPoFB54+oOz4wsleOKLptNBU=", "/home/fanju/media/uploaded_images/2012/11/06/file_1.50x50_q85_crop_detail.jpg")
#    def publishAvatar(self):
#        def processResult(result):
#            print type(result)
#            print result.toXml()
#            return result
#            
#        iq = IQ(self.xmlstream, 'set')
#        iq['from']='xuaxu@fanjoin.com'
#        pubsub = iq.addElement((NS_AVATAR, 'pubsub'))
#        publish = pubsub.addElement('publish')
#        publish['node'] = 'urn:xmpp:avatar:data'
#        item = publish.addElement('item')
#        item['id'] = '111f4b3c50d7b0df729d299bc6f8e9ef9066971f'
#        item.addElement('data', 'urn:xmpp:avatar:data', content='qANQR1DBwU4DX7jmYZnncm')
#        d = iq.send()
#        d.addCallback(processResult)
#        return d

