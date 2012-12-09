from django.conf import settings
from twisted.application import service
from twisted.internet import reactor
from twisted.python import log
from twisted.words.protocols.jabber.jid import JID
from wokkel import client
from wokkel.client import XMPPClient, XMPPClientConnector
from wokkel.compat import IQ
from wokkel.subprotocols import XMPPHandler
from wokkel.xmppim import Presence
import hashlib
import logging

logger = logging.getLogger('api')

def clientCreator(factory, host=None):
    if not host:
        domain = factory.authenticator.jid.host
    else:
        domain = host
    c = XMPPClientConnector(reactor, domain, factory)
    c.connect()
    return factory.deferred

class AvatarUpdatedPresence(Presence):
    def __init__(self, sender, sha1):
        Presence.__init__(self)
        self['from']=sender
        x = self.addElement(('vcard-temp:x:update', 'x'))
        x.addElement('photo', content=sha1) 

NS_AVATAR='http://jabber.org/protocol/pubsub'
NS_VCARD_AVATAR='vcard-temp'
NS_ROSTER_ITEM='jabber:iq:roster'
        
def addOrUpdateRosterItem(jid, name, xmlstream):       
    iq = IQ(xmlstream, 'set')
    iq.addElement((NS_ROSTER_ITEM, 'query'))
    item = iq.query.addElement('item')
    item['jid'] = jid
    item['name'] = name
    item['subscription']='both'
    d = iq.send()
    return d

        
def publishvCardAvatar(jid, avatar, xmlstream):
    def processvCardAvatarUpdateResult(result):
        avatarUpdatedNotif = AvatarUpdatedPresence(jid, avatar_sha1)
        xmlstream.send(avatarUpdatedNotif.toXml())
        
    iq = IQ(xmlstream, 'set')
    iq['from']=jid
    vCard = iq.addElement((NS_VCARD_AVATAR, 'vCard'))
    photo = vCard.addElement('PHOTO')
    photo.addElement('TYPE', content='image/jpeg')
    content = open(avatar, "rb").read().encode("base64")
    avatar_sha1 = hashlib.sha1(content).hexdigest()
    photo.addElement('BINVAL', content=content)
    d = iq.send()
    d.addCallback(processvCardAvatarUpdateResult)
    return d

def syncName(username, password, name):
    logger.debug("sync name of user '%s' to %s" % (username, name))
    jidStr = username + "@fanjoin.com"
    jid = JID(jidStr)
    factory = client.DeferredClientFactory(jid, password)    
    factory.streamManager.logTraffic = True
    d = clientCreator(factory,"42.121.34.164")
    d.addCallback(lambda _ : addOrUpdateRosterItem(jidStr, "Wayne1234", factory.streamManager.xmlstream) )
    d.addBoth(lambda _: reactor.callLater(1, reactor.stop))
    d.addErrback(log.err)
    reactor.run()


def syncAvatar(username, password, avatar):
    logger.debug("sync avatar of user '%s'" % username)
    jidStr = username + "@fanjoin.com"
    jid = JID(jidStr)
    factory = client.DeferredClientFactory(jid, password)    
    d = clientCreator(factory, "42.121.34.164")
    d.addCallback(lambda _ : publishvCardAvatar(jidStr, avatar, factory.streamManager.xmlstream) )
    d.addErrback(log.err)
    d.addBoth(lambda _: reactor.callLater(1, reactor.stop))
    reactor.run()

def syncBoth(user_profile):
    syncName(user_profile.user.username, user_profile.user.password, user_profile.name)
    if user_profile.avatar:
        syncAvatar(user_profile.user.username, user_profile.user.password, user_profile.small_avatar_path)

#syncName("xuaxu","qqqqqq","Waynexyz")
#syncAvatar("xuaxu","qqqqqq","/home/fanju/media/uploaded_images/2012/09/11/abc.com_avatar.jpg.50x50_q85_crop_detail.jpg")
#reactor.run()    
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

