from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from eo.models import UserProfile

class WeiboAuthenticationBackend(object):
    def authenticate(self, **credentials):
        token = credentials.get('token')
        weibo_id = credentials.get('weibo_id')
        if token and weibo_id:
            try:
                user_profile = UserProfile.objects.get(weibo_access_token=token)
                user = user_profile.user
            except ObjectDoesNotExist:
                username,password='weibo_%s' % weibo_id, User.objects.make_random_password()
                user = User.objects.create_user(username, '', password)
                user_profile = user.get_profile()
                user_profile.weibo_id = weibo_id
                user_profile.weibo_access_token = token
                # user_profile.avatar = TODO save avatar, motto, etc 
                user_profile.save()
            return user
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None