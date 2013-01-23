from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from eo import util
import logging
 
logger = logging.getLogger('api') 
pyapns_wrapper = util.PyapnsWrapper(settings.APNS_HOST,
                            settings.APP_ID,
                            settings.APNS_CERTIFICATE_LOCATION)

class Command(BaseCommand):
    def handle(self, *args, **options):
        logging.debug("Handle offline message") 
        sender = args[0]
        receiver = args[1]
        message = args[2]  
        unread_count = int(args[3])
        if len(message) > 160:
            message = message[0:160] + " ... "
  
        fromUser = User.objects.get(username=util.escape_xmpp_username(sender)).get_profile()
        toUser = User.objects.get(username=util.escape_xmpp_username(receiver)).get_profile()
        logger.info("%s->%s: %s" % (fromUser, toUser, message)) 
        
        if toUser.apns_token:
            logger.debug("pushing message to %s from %s(%d unread)" % (toUser.name, fromUser.name, unread_count))
            pyapns_wrapper.notify(toUser.apns_token, "%s: %s" % (fromUser.name, message.decode("utf-8")), unread_count )     
        return ""   