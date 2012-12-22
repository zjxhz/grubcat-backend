from django.core.management.base import BaseCommand
from erlport import Port, Protocol, String
import logging
import util
from django.conf import settings
 
logger = logging.getLogger('api') 
pyapns_wrapper = util.PyapnsWrapper(settings.APNS_HOST,
                            settings.APP_ID,
                            settings.APNS_CERTIFICATE_LOCATION)

class Command(BaseCommand, Protocol):
    def handle(self, *args, **options):
        proto = ProcessProtocol()
        logging.debug("Handle") 
        proto.run(Port(use_stdio=True, packet=4))        
 
class ProcessProtocol(Protocol):
    def handle_message(self, fromUser, toUser, message):
        toUser = String(toUser)
        message = String(message)
        fromUser = String(fromUser)
        
        toUser = toUser.split('@')[0]
        fromUser = fromUser.split('/')[0]
               
        if len(message) > 160:
            message = message[0:160] + " ... "
        logger.info("%s->%s: %s" % (fromUser, toUser, message))
#        if toUser.apns_token:
#            pyapns_wrapper.notify(toUser.apns_token, "%s: %s" % message);
#        recp = User.objects.get(screenname=toUser)
#        if recp.iphone_device_token:
#            logging.debug("Called Push Notification Service(int)") 
#            sendToUser.delay(recp.iphone_device_token, toUser, message, 'friend')
#            sendToUserDev.delay(recp.iphone_device_token, toUser, message, 'friend')
            
        return ""