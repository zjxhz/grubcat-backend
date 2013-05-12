# Tunnel - TODO
#
# (C) 2010 Luke Slater, Steve 'Ashcrow' Milner
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from django.contrib import auth
from django.contrib.auth.models import User, check_password
from django.core.management.base import BaseCommand
from fanju import util
import logging
import struct
import sys
"""
Authenticate XMPP user.
"""
 
logger = logging.getLogger('api') 
 
class Command(BaseCommand):
    """
    Acts as an auth service for ejabberd through ejabberds external auth
    option. See contrib/ejabberd/ejabber.cfg for an example configuration.
    """
    
    help = "Runs an ejabberd auth service"
    
    def __init__(self, *args, **kwargs):
        """
        Creation of the ejabberd atuh bridge service.
        """
        BaseCommand.__init__(self, *args, **kwargs)
        logger.info(('ejabberd_auth_bridge process started (more than one is common)'))
 
    def _generate_response(self, success=False):
        """
        Creates and sends a response back to the ejabberd server.
 
        :Parameters
           - `success`: boolean if we should respond successful or not
        """
        result = 0
        if success:
            result = 1
        sys.stdout.write(struct.pack('>hh', 2, result))
        sys.stdout.flush()
 
    def _handle_isuser(self, username):
        """
        Handles the isuer ejabberd command.
 
        :Parameters:
           - `username`: the user name to verify exists
        """
        try:
            logger.info("checking if %s is a valid user" % username)
            User.objects.get(username=username)
            self._generate_response(True)
        except User.DoesNotExist:
            self._generate_response(False)
 
    def _handle_auth(self, username, password):
        """
        Handles authentication of the user.
 
        :Parameters:
           - `username`: the username to verify
           - `password`: the password to verify with the user
        """
        try:
            # password can be the hash one when the request is initiated from django(e.g. to sync avatar and name) where the original password is unknown, 
            # or the raw one when the request is from client
            logger.debug("auth for user: %s" % username)
            user = User.objects.get(username=username)
            if password == user.password or check_password(password, user.password):
                self._generate_response(True)
                logger.info(username + ' has logged in from ejabberd')
            elif username.startswith("weibo_"):
                logger.debug("verifying a weibo user")
                dic = {"username":username, "access_token":password}
                if auth.authenticate(**dic):
                    self._generate_response(True)
                    logger.info(username + ' has logged in from ejabberd')
                else:
                    self._generate_response(False)
                    logger.info(username + ' (a weibo user ) failed to log in from ejabberd')
            else:
                self._generate_response(False)
                logger.info(username + ' failed auth from ejabberd, incorrect password: %s' % password)
        except User.DoesNotExist:
            self._generate_response(False)
            logger.info(username + ' is not a valid user from ejabberd')
 
    def handle(self, *args, **options):
        """
        How to check if a user is valid
 
        :Parameters:
           - `options`: keyword arguments
        """
        try:
            while True:
                # Verify the information checks out
                try:
                    length = sys.stdin.read(2)
                    size = struct.unpack('>h', length)[0]
                    logger.debug('Got data of size ' + str(size))
                    input_ejabberd = sys.stdin.read(size).split(':')
                    operation = input_ejabberd.pop(0)
                    username = util.escape_xmpp_username(input_ejabberd[0])
                    
                except Exception:
                    # It wasn't even in the right format if we get here ...
                    self._generate_response(False)
        #                    continue
                if operation == 'auth':
                    logger.debug('Auth request being processed for ' + username)
                    self._handle_auth(username, input_ejabberd[2])
                elif operation == 'isuser':
                    logger.debug('Asked if ' + username + ' is a user')
                    self._handle_isuser(username)
                elif operation == 'setpass':
                    logger.debug('Asked if to change password for ' + username)
                    self._generate_repsonse(False)
        except KeyboardInterrupt:
            raise SystemExit(0)
        
    def __del__(self):
        """
        What to do when we are shut off.
        """
        logger.info('ejabberd_auth_bridge process stopped')
