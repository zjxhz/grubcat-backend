from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from eo.models import UserProfile
import traceback
import urllib2

class WeiboAuthenticationBackend(object):
    def authenticate(self, **credentials):
        token = credentials.get('access_token')
        weibo_id = credentials.get('weibo_id')
        user_to_authenticate = None # tell python this is a local variable
        if token and weibo_id:
            try:
                user_profile = UserProfile.objects.get(weibo_access_token=token)
                user_to_authenticate = user_profile.user
            except ObjectDoesNotExist:
                try:
                    username,password='weibo_%s' % weibo_id, User.objects.make_random_password()
                    user_to_authenticate = User.objects.create_user(username, '', password)
                    user_profile = user_to_authenticate.get_profile()
                    user_profile.weibo_id = weibo_id
                    user_profile.weibo_access_token = token
                    user_profile.name = credentials.get('name')
                    user_profile.motto = credentials.get('motto') #description
                    user_profile.gender = int(credentials.get('gender')) 
                    avatar_url = credentials.get('avatar') 
                    user_profile.avatar.save(username+".jpg", ContentFile(urllib2.urlopen(avatar_url).read()), save=False)
                    user_profile.save()
                except Exception as e:
                    if user_to_authenticate:
                        user_to_authenticate.delete()
                    traceback.print_exc()
                    raise e
            return user_to_authenticate
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None