from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from grubcat.eo import util
import logging
import os
import json

logger = logging.getLogger('api')
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

        sender = data["sender"]
        receiver = data["receiver"]
        message = data["message"]
        unread_count = int(data["unread"])
        if len(message) > 160:
            message = message[0:160] + " ... "

        fromUser = User.objects.get(username=util.escape_xmpp_username(sender)).get_profile()
        toUser = User.objects.get(username=util.escape_xmpp_username(receiver)).get_profile()
        message_utf8=message.encode("utf-8")
        logger.info("%s->%s: %s" % (fromUser, toUser, message_utf8))

        if toUser.apns_token:
            receiver_name_utf8 = toUser.name.encode("utf-8")
            sender_name_utf8 = fromUser.name.encode("utf-8")
            logger.debug("pushing message to %s from %s(%d unread)" % (receiver_name_utf8, sender_name_utf8, unread_count))
            message_to_user="%s: %s" % (sender_name_utf8, message_utf8)
            pyapns_wrapper.notify(toUser.apns_token, message_to_user, unread_count )

        os.remove(f)   
        return ""