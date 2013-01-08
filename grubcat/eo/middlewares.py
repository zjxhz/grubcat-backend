from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from eo.models import UserProfile, Gender
import json
import logging
import urllib2
import weibo

logger = logging.getLogger("api")

class WeiboAuthenticationBackend(object):
    def authenticate(self, **credentials):
        user_to_authenticate = None # tell Python explicitly this is a local variable
        
        access_token =credentials.get('access_token')
        if not access_token:
            raise
        expires_in = credentials.get('expires_in')
        if not expires_in:
            expires_in = str(3600*24*14)
        weibo_client = weibo.APIClient(app_key=settings.WEIBO_APP_KEY, app_secret=settings.WEIBO_APP_SECERT,redirect_uri=settings.WEIBO_REDIRECT_URL)
        weibo_client.set_access_token(access_token, expires_in)
        
        if UserProfile.objects.filter(weibo_access_token=access_token).count():
            user_profile = UserProfile.objects.get(weibo_access_token=access_token)
            logger.debug("auth for %s OK" % user_profile)
            user_to_authenticate = user_profile.user
        else:
            try:
                logger.debug("access_token no match, a new weibo user or access_token has expired")
                weibo_id = weibo_client.account.get_uid.get()["uid"]
                if UserProfile.objects.filter(weibo_id=weibo_id).count():
                    logger.debug("access_token found, update access token so next time it would be faster")
                    user_profile = UserProfile.objects.get(weibo_id=weibo_id)
                    user_profile.weibo_access_token=access_token
                    user_profile.save()
                    user_to_authenticate = user_profile.user
                    return user_to_authenticate
                else:
                    logger.debug("Probably a new weibo user, create a new user for it")
                    username,password='weibo_%s' % weibo_id, User.objects.make_random_password()
                    user_to_authenticate = User.objects.create_user(username, '', password)
                    user_to_authenticate.is_active = False #set unactive before complete some profile
                    user_to_authenticate.save()
                    user_profile = user_to_authenticate.get_profile()
                    user_data = weibo_client.users.show.get(uid=weibo_id)
                    user_profile.weibo_id = weibo_id
                    user_profile.weibo_access_token = access_token
                    user_profile.name = user_data.get('name')
                    user_profile.motto = user_data.get('description') 
                    if user_data.get('gender') == "m":
                        user_profile.gender = Gender.MALE
                    elif user_data.get('gender') == "f":
                        user_profile.gender = Gender.FEMALE
                    avatar_url = user_data.get('avatar_large') 
                    user_profile.avatar.save(username+".jpg", ContentFile(urllib2.urlopen(avatar_url).read()), save=False)
                    user_profile.save()
                    return user_to_authenticate
            except Exception as e:
                if user_to_authenticate:
                    user_to_authenticate.delete()
                logger.exception("failed to auth %s " % user_to_authenticate)
                raise Exception(u'微博接口异常')
            
        return user_to_authenticate
        
        
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
