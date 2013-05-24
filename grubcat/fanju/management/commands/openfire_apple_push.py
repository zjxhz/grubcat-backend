from django.conf import settings
from django.core.management.base import BaseCommand
from fanju import util
from fanju.models import User
import json
import logging
import os

logger = logging.getLogger(__name__)
pyapns_wrapper = util.PyapnsWrapper(settings.APNS_HOST,
                            settings.APP_ID,
                            settings.APNS_CERTIFICATE_LOCATION)

class Command(BaseCommand):
    def handle(self, *args, **options):
        logging.debug("Handle offline message")
        f = open(args[0], "r")
        logger.debug("open %s for reading " % f)
        content = f.read();
        data = json.loads(content)
        f.close();


        receiver = data["receiver"]
        message = data["message"]
        unread_count = int(data["unread"])
        if len(message) > 160:
            message = message[0:160] + " ... "


        toUser = User.objects.get(username=util.escape_xmpp_username(receiver))
        message_utf8=message.encode("utf-8")

        logger.debug("about to push to user %s with apns_token: %s" % (receiver, toUser.apns_token) )
        if toUser.apns_token:
            receiver_name_utf8 = toUser.name.encode("utf-8")
            if data["type"] == "chat":
                sender = data["sender"]
                fromUser = User.objects.get(username=util.escape_xmpp_username(sender))
                logger.info("%s->%s: %s" % (fromUser, toUser, message_utf8))
                sender_name_utf8 = fromUser.name.encode("utf-8")
                message_to_user="%s: %s" % (sender_name_utf8, message_utf8)
                logger.debug("pushing message to %s from %s(%d unread)" % (receiver_name_utf8, sender_name_utf8, unread_count))
            else:
                logger.debug("pushing an event")
                message_to_user= message_utf8
            pyapns_wrapper.notify(toUser.apns_token, message_to_user, unread_count )

        # os.remove(f)   TODO enable this again in production, it is here now for easy debugging
        return ""