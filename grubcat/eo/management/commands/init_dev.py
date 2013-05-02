from django.conf import settings
from django.core.management.base import BaseCommand
from eo.models import Meal, UserProfile
from optparse import make_option
import os
from random import randint

class Command(BaseCommand):
    """
    Init dev DB so that the resources will point to correct locations, this is needed if the images are dumped from server while
    the resources are not
    options: 
        meal_photo: which is assumed located at %suploaded_images/
    """    
    option_list = BaseCommand.option_list + ( make_option('--meal_photo'), \
                                              make_option('--avatar', action="store_true", dest="avatar"),
                                              make_option('--photo', action="store_true", dest="photo"),)
    
    def handle(self, *args, **options):
        meal_photo = options.get("meal_photo")
        if meal_photo:
            meal_photo_path = "%suploaded_images/%s" % (settings.MEDIA_ROOT, meal_photo) 
            if not os.path.exists(meal_photo_path):
                print u"%s does not exist, skip setting meal photo" % meal_photo_path
            else:
                print "checking meal photos"
                for meal in Meal.objects.all():
                    if not meal.photo or not os.path.exists(meal.photo.path):
                        print u"meal %s has no photo or the photo does not exist" % meal.id
                        meal.photo = "uploaded_images/%s" % meal_photo
                        meal.save()
                        
        avatar = options.get("avatar")
        if avatar:
            available_avatars = self.available_avatars() 
            if not available_avatars:
                print u"no available avatar under %suploaded_images/" % settings.MEDIA_ROOT
            else:
                print "checking avatars"
                for user in UserProfile.objects.all():
                    if not user.avatar or not os.path.exists(user.avatar.path):
                        print u"user %s has no avatar or the avatar does not exist" % user.id
                        random_index = randint(0, len(available_avatars) - 1)
                        user.avatar = available_avatars[random_index]
                        user.save()
        photo = options.get("photo")
        if photo:
            available_photos = self.available_avatars()  # same as avatar
            if not available_photos:
                print u"no available photo under %suploaded_images/" % settings.MEDIA_ROOT
            else:
                print "checking photo"
                for user in UserProfile.objects.all():
                    for p in user.photos.all():
                        if not os.path.exists(p.photo.path):
                            print u"photo %s does not exist" % p.id
                            random_index = randint(0, len(available_avatars) - 1)
                            p.photo = available_avatars[random_index]
                            p.save()
                        
    def available_avatars(self):
        avatars = []
        for dirname, dirnames, filenames in os.walk('%suploaded_images/' % settings.MEDIA_ROOT):
            for filename in filenames:
                path = os.path.join(dirname, filename)
                if ".jpg" in path and not "crop" in path: #a cropped image
                    avatars.append(path[len(settings.MEDIA_ROOT):])
        return avatars