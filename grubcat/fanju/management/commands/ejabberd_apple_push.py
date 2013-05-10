from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from fanju import util
from erlport import Port, Protocol, String
import logging
 
logger = logging.getLogger('api') 
pyapns_wrapper = util.PyapnsWrapper(settings.APNS_HOST,
                            settings.APP_ID,
                            settings.APNS_CERTIFICATE_LOCATION)

class Command(BaseCommand, Protocol):
    def handle(self, *args, **options):
        proto = ProcessProtocol()
        logging.debug("Handle offline message") 
        proto.run(Port(use_stdio=True, packet=4))        
 
class ProcessProtocol(Protocol):
    def handle_message(self, fromUser, toUser, message):
        toUser = String(toUser).split('@')[0]
        message = String(message)
        fromUser = String(fromUser).split('@')[0]
        if len(message) > 160:
            message = message[0:160] + " ... "
          
        logger.info("%s->%s: %s" % (fromUser, toUser, message))
          
        fromUser = User.objects.get(username=util.escape_xmpp_username(fromUser))
        toUser = User.objects.get(username=util.escape_xmpp_username(toUser))
               
        
        if toUser.apns_token:
            logger.debug("pushing message to %s from %s" % (toUser.name, fromUser.name))
            pyapns_wrapper.notify(toUser.apns_token, "%s: %s" % (fromUser.name, message), 1 ) #TODO now badge is always 1. should be recorded somewhere    
        return ""