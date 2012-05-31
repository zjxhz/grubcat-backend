from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.query_utils import Q
from django.db.models.signals import post_save
from image_cropping.fields import ImageRatioField, ImageCropField

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=135)
    def __unicode__(self):
        return u'%s' % (self.name)
    class Meta:
        db_table = u'company'

class RestaurantTag(models.Model):
    name = models.CharField(max_length=45)
    class Meta:
        db_table = u'restaurant_tag'
    def __unicode__(self):
        return u'%s' % (self.name)


class Region(models.Model):
    name = models.CharField(max_length=64)
    def __unicode__(self):
        return u'%s' % (self.name)
    class Meta:
        db_table = u'region'

class Restaurant(models.Model):
    name = models.CharField(max_length=135)
    address = models.CharField(max_length=765)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    tel = models.CharField(max_length=60)
    tel2 = models.CharField(max_length=60, blank=True)
    introduction = models.CharField(max_length=6000, blank=True)
    phone_img_url = models.CharField(max_length=1024, blank=True)
    average_cost = models.IntegerField()
    rating = models.IntegerField()
    company = models.ForeignKey(Company)
    tags = models.ManyToManyField(RestaurantTag)
    regions = models.ManyToManyField(Region)
    def __unicode__(self):
        return u'%s %s' % (self.name, self.address)
    def get_recommended_dishes(self, max_number=10):
        return BestRatingDish.objects.filter(restaurant__id=self.id).order_by('-times')[:max_number]
    def get_rating(self):
        return Rating.objects.filter(restaurant__id=self.id)
    def get_average_cost(self):
        '''ri = RestaurantInfo.objects.get(restaurant__id=self.id)
        return ri.average_cost'''
        return self.average_cost
    '''def get_rating(self):
        ri = RestaurantInfo.objects.get(restaurant__id=self.id)
        return ri.rating
        return rating'''
    class Meta:
        db_table = u'restaurant'

class RestaurantInfo(models.Model):
    restaurant = models.OneToOneField(Restaurant, related_name='info')
    average_cost = models.FloatField()
    average_rating = models.FloatField()
    good_rating_percentage = models.FloatField()
    divider = models.IntegerField()
    class Meta:
        db_table = u'restaurant_info'

class RatingPic(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    user = models.ForeignKey(User)
    image = models.CharField(max_length=1024)
    class Meta:
        db_table = u'rating_pic'

class Menu(models.Model):
    restaurant = models.OneToOneField(Restaurant)
    cover = models.CharField(max_length=255, null=True)
    menu_timestamp = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = u'menu'

class DishTag(models.Model):
    name = models.CharField(max_length=15)
    def __unicode__(self):
        return u'%s' % (self.name)
    class Meta:
        db_table = u'dish_tag'

class DishCategory(models.Model):
    menu = models.ForeignKey(Menu, related_name="categories")
    name = models.CharField(max_length=45)
    parent_category = models.ForeignKey('self', null=True)
    def __unicode__(self):
        return u'%s' % (self.name)
    class Meta:
        db_table = u'dish_category'

class Dish(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=135)
    pic = models.CharField(max_length=765, blank=True)
    price = models.FloatField()
    restaurant = models.ForeignKey(Restaurant)
    menu = models.ForeignKey(Menu, related_name='dishes', null=True)
    ingredient = models.CharField(max_length=765, blank=True)
    cooking = models.CharField(max_length=765, blank=True)
    taste = models.CharField(max_length=18)
    uom = models.CharField(max_length=30)
    has_other_uom = models.IntegerField(default=0)
    available = models.IntegerField(default=0)
    is_mandatory = models.IntegerField(default=0)
    is_recommended = models.IntegerField(default=0)
    tags =  models.ManyToManyField(DishTag)
    categories = models.ManyToManyField(DishCategory)
    class Meta:
        db_table = u'dish'

class DishOtherUom(models.Model):
    price = models.DecimalField(max_digits=11, decimal_places=0)
    uom = models.CharField(max_length=10)
    dish = models.ForeignKey(Dish, related_name='other_uom')
    class Meta:
        db_table = u'dish_other_uom'


class Rating(models.Model):
    user = models.ForeignKey(User, related_name='user_ratings')
    restaurant = models.ForeignKey(Restaurant, related_name="ratings")
    comments = models.CharField(max_length=4096)
    time = models.DateTimeField()
    rating = models.FloatField()
    average_cost = models.FloatField()
    dishes = models.ManyToManyField(Dish, db_table="rating_dishes")
    auto_share = models.BooleanField()
    # for average cost, see RestaurantAverageCost
    class Meta:
        db_table = u'rating'

class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    customer = models.ForeignKey('UserProfile', related_name='orders')
    #meal = models.OneToOneField('Meal', null=True)
    num_persons = models.IntegerField()
    status = models.IntegerField()
    total_price = models.FloatField()
    created_time = models.DateTimeField()
    confirmed_time = models.DateTimeField(null=True)
    completed_time = models.DateTimeField(null=True)
    table = models.CharField(max_length=20)
    dishes = models.ManyToManyField(Dish, through='OrderDishes')
    class Meta:
        db_table = u'order'

class OrderDishes(models.Model):
    order = models.ForeignKey(Order)
    dish = models.ForeignKey(Dish)
    quantity = models.FloatField()
    class Meta:
        db_table = u'order_dishes'

class Relationship(models.Model):
    from_person = models.ForeignKey("UserProfile", related_name='from_user')
    to_person = models.ForeignKey("UserProfile", related_name='to_user')
    status = models.IntegerField(default=0) # FOLLOWING, BLOCKED

    def __unicode__(self):
        return '%s -> %s: %s' % (self.from_person, self.to_person, self.status)

    class Meta:
        db_table = u'relationship'


class UserLocation(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    updated_at = models.DateTimeField()
    class Meta:
        db_table = u"user_location"

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    favorite_restaurants = models.ManyToManyField(Restaurant,db_table="favorite_restaurants", related_name="user_favorite")
    following = models.ManyToManyField('self', related_name="related_to", symmetrical=False, through="RelationShip")
    recommended_following = models.ManyToManyField('self', symmetrical=False, db_table="recommended_following")
    gender = models.IntegerField(null=True)
    avatar = models.CharField(max_length=256) # photo
    location = models.ForeignKey(UserLocation, unique=True, null=True)
    constellation = models.IntegerField(null=True, default=-1)
    birthday = models.DateTimeField(null=True)
    college = models.CharField(max_length=64, null=True)
    work_for = models.CharField(max_length=64, null=True)
    occupation = models.CharField(max_length=64, null=True)
    @property
    def followers(self):
        return self.related_to.all()
    @property
    def meals(self):
        return Meal.objects.filter(Q(host=self) | Q(participants=self))
    @property
    def invitations(self):
        """ Invitation sent from others.
        """
        return MealInvitation.objects.filter(to_person=self).filter(status=0)

    @property
    def avatar_default_if_none(self):
        if self.avatar:
            return self.avatar
        else:
            return "/uploaded_images/anno.png"
    def __unicode__(self):
        return self.user.username
    class Meta:
        db_table = u'user_profile'



class UserMessage(models.Model):
    from_person = models.ForeignKey(UserProfile, related_name="sent_from_user")
    to_person = models.ForeignKey(UserProfile, related_name='sent_to_user')
    message = models.CharField(max_length=1024)
    timestamp = models.DateTimeField()
    type = models.IntegerField(default=0) # 0 message, 1 comments
    class Meta:
        db_table = u'user_message'


# Create a user profile if the profile does not exist
def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)

class BestRatingDish(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name="best_rating_dishes")
    dish = models.ForeignKey(Dish)
    times = models.IntegerField()
    class Meta:
        db_table = u'best_rating_dish'

class Meal(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    order = models.OneToOneField(Order, null=True)
    topic = models.CharField(max_length=64)
    introduction = models.CharField(max_length=1024)
    list_price = models.IntegerField()
    photo = models.FileField(null=True, upload_to='uploaded_images/%Y/%m/%d')
    time = models.DateTimeField()
    host = models.ForeignKey(UserProfile, null=True, related_name="host_user")
    participants = models.ManyToManyField(UserProfile)
    actual_persons = models.IntegerField(default=1, null=True)
    min_persons = models.IntegerField()
    max_persons = models.IntegerField(default=0, null=True) # not used for now, min_persons = max_persons
    type = models.IntegerField() # THEMES, DATES
    privacy = models.IntegerField(default=0) # PUBLIC, PRIVATE, VISIBLE_TO_FOLLOWERS?
    def is_participant(self, user_profile):
        for participant in self.participants.all(): #TODO query the user by id to see the if the user exist
            if participant == user_profile:
                return True
        return False

    @property
    def left_persons(self):
        return self.max_persons  - self.actual_persons

    @models.permalink
    def get_absolute_url(self):
        return 'meal_view', [str(self.id)]

    class Meta:
        db_table = u'meal'

class MealInvitation(models.Model):
    from_person = models.ForeignKey(UserProfile, related_name="invitation_from_user")
    to_person = models.ForeignKey(UserProfile, related_name='invitation_to_user')
    meal = models.ForeignKey(Meal)
    timestamp = models.DateTimeField(default=datetime.now())
    status = models.IntegerField(default=0) # PENDING, ACCEPTED, REJECTED

    def is_related(self, user_profile):
        return self.from_person==user_profile or self.to_person==user_profile

    class Meta:
        db_table = u'meal_invitation'

class ImageTest(models.Model):
    image = ImageCropField(blank=True, null=True, upload_to='apps')
    # size is "width x height"
    cropping = ImageRatioField('image', '430x360')

'''
class CategoryRestaurant(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    parent_category = models.ForeignKey('self', null=True, blank=True)
    class Meta:
        db_table = u'category_restaurant'

class DishOtherUom(models.Model):
    id = models.IntegerField(primary_key=True)
    price = models.DecimalField(max_digits=11, decimal_places=0)
    uom = models.CharField(max_length=30)
    dish = models.ForeignKey(Dish)
    restaurant = models.ForeignKey(Dish)
    class Meta:
        db_table = u'dish_other_uom'

class Table(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    class Meta:
        db_table = u'table'
'''

class OrderStatus:
    CREATED = 1
    CONFIRMED = 2
    PAIED = 3
    COMPLETED = 4
    
