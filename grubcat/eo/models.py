from django.db import models
from django.contrib.auth.models import User
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
     

class BusinessDistrict(models.Model):
    name = models.CharField(max_length=64)
    def __unicode__(self):
        return u'%s' % (self.name)
    class Meta:
        db_table = u'business_district'
        
class Restaurant(models.Model):
    name = models.CharField(max_length=135)
    address = models.CharField(max_length=765)
    longitude = models.FloatField()
    latitude = models.FloatField()
    tel = models.CharField(max_length=60)
    tel2 = models.CharField(max_length=60, blank=True)
    introduction = models.CharField(max_length=6000, blank=True)
    phone_img_url = models.CharField(max_length=1024, blank=True)
    average_cost = models.IntegerField()
    rating = models.IntegerField()
    company = models.ForeignKey(Company)
    tags = models.ManyToManyField(RestaurantTag)
    business_districts = models.ManyToManyField(BusinessDistrict)
    def __unicode__(self):
        return u'%s %s' % (self.name, self.address)
    def get_recommended_dishes(self, max_number=10):
        return RecommendedDishes.objects.filter(restaurant__id=self.id).order_by('-times')[:max_number]
    def get_comments(self):
        return RestaurantComments.objects.filter(restaurant__id=self.id)
    def get_average_cost(self):
        '''ri = RestaurantInfo.objects.get(restaurant__id=self.id)
        return ri.average_cost'''
        return average_cost
    def get_rating(self):
        '''ri = RestaurantInfo.objects.get(restaurant__id=self.id)
        return ri.rating'''
        return rating
    class Meta:
        db_table = u'restaurant'
        
class RestaurantComments(models.Model):
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant)
    comments = models.CharField(max_length=4096)
    time = models.DateTimeField()
    rating = models.FloatField()
    average_cost = models.FloatField()
    # for average cost, see RestaurantAverageCost
    class Meta:
        db_table = u'restaurant_comments'

class RestaurantInfo(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    average_cost = models.FloatField()
    average_rating = models.FloatField()
    good_rating_percentage = models.FloatField()
    divider = models.IntegerField()
    class Meta:
        db_table = u'restaurant_info'

class UserSharedImages(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    user = models.ForeignKey(User)
    image = models.CharField(max_length=1024)
    class Meta:
        db_table = u'user_shared_images'
        
class Menu(models.Model):
    restaurant = models.OneToOneField(Restaurant)
    cover = models.CharField(max_length=255, blank=True)
    menu_timestamp = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = u'menu'

class TagDish(models.Model):
    name = models.CharField(max_length=15)
    def __unicode__(self):
        return u'%s' % (self.name)
    class Meta:
        db_table = u'tag_dish'

class CategoryDish(models.Model):
    menu = models.ForeignKey(Menu)
    name = models.CharField(max_length=45)
    parent_category = models.ForeignKey('self', null=True)
    def __unicode__(self):
        return u'%s' % (self.name)
    class Meta:
        db_table = u'category_dish'
        
class Dish(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=135)
    pic = models.CharField(max_length=765, blank=True)
    price = models.FloatField()
    restaurant = models.ForeignKey(Restaurant)
    ingredient = models.CharField(max_length=765, blank=True)
    cooking = models.CharField(max_length=765, blank=True)
    taste = models.CharField(max_length=18)
    uom = models.CharField(max_length=30)
    has_other_uom = models.IntegerField(default=0)
    available = models.IntegerField(default=0)
    is_mandatory = models.IntegerField(default=0)
    is_recommended = models.IntegerField(default=0)
    tags =  models.ManyToManyField(TagDish)
    categories = models.ManyToManyField(CategoryDish)
    class Meta:
        db_table = u'dish'

class DishOtherUom(models.Model):
    price = models.DecimalField(max_digits=11, decimal_places=0)
    uom = models.CharField(max_length=10)
    dish = models.ForeignKey(Dish)
    class Meta:
        db_table = u'dish_other_uom'

class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    customer = models.ForeignKey(User)
    num_persons = models.IntegerField()
    status = models.IntegerField()
    total_price = models.DecimalField(max_digits=11, decimal_places=2)
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
    class Meta:
        db_table = u'relationship'
    
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    favorite_restaurants = models.ManyToManyField(Restaurant)
    following = models.ManyToManyField('self', related_name="related_to", symmetrical=False, through="RelationShip")
    recommended_following = models.ManyToManyField('self', symmetrical=False)
    gender = models.IntegerField()
    avatars = models.CharField(max_length=256)
    lat = models.FloatField()
    lng = models.FloatField()
    location_updated_at = models.DateTimeField()
    constellation = models.IntegerField()
    birthday = models.DateTimeField()
    college = models.CharField(max_length=64)
    work_for = models.CharField(max_length=64)
    profesion = models.CharField(max_length=64)
    @property
    def followers(self):
        return self.related_to.all()
    def __unicode__(self):
        return self.user.name
    class Meta:
        db_table = u'user_profile'

class UserMessage(models.Model):
    from_person = models.ForeignKey(UserProfile, related_name="sent_from_user")
    to_person = models.ForeignKey(UserProfile, related_name='sent_to_user')
    message = models.CharField(max_length=1024)
    timestamp = models.DateTimeField()
    message_type = models.IntegerField(default=0) # 0 message, 1 comments
    class Meta:
        db_table = u'user_message'


# Create a user profile if the profile does not exist
def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User)

class RecommendedDishes(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    dish = models.ForeignKey(Dish)
    times = models.IntegerField()
    class Meta:
        db_table = u'recommended_dishes'
        

class ImageTest(models.Model):
    image = ImageCropField(blank=True, null=True, upload_to='uploaded_images/%Y/%m/%d')
    # size is "width x height"
    cropping = ImageRatioField('image', '430x360')
'''
class CategoryRestaurant(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    parent_category = models.ForeignKey('self', null=True, blank=True)
    class Meta:
        db_table = u'category_restaurant'

class Customer(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    class Meta:
        db_table = u'customer'

class DishCategory(models.Model):
    category_id = models.IntegerField(primary_key=True)
    dish = models.ForeignKey(Dish)
    restaurant = models.ForeignKey(Dish)
    class Meta:
        db_table = u'dish_category'

class DishHasCategory(models.Model):
    dish = models.ForeignKey(Dish)
    restaurant = models.ForeignKey(Dish)
    category = models.ForeignKey(CategoryDish)
    class Meta:
        db_table = u'dish_has_category'

    
class TagDish(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    class Meta:
        db_table = u'tag_dish'
    
class DishHasTag(models.Model):
    dish = models.ForeignKey(Dish)
    restaurant = models.ForeignKey(Dish)
    tag = models.ForeignKey(TagDish)
    class Meta:
        db_table = u'dish_has_tag'

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
    
class OrderHasDish(models.Model):
    order = models.ForeignKey(Order)
    customer = models.ForeignKey(Order)
    table = models.ForeignKey(Order)
    dish = models.ForeignKey(Dish)
    restaurant = models.ForeignKey(Dish)
    quantity = models.DecimalField(max_digits=11, decimal_places=0)
    uom = models.CharField(max_length=30)
    comments = models.CharField(max_length=135, blank=True)
    class Meta:
        db_table = u'order_has_dish'

class RestaurantHasCategory(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    category = models.ForeignKey(CategoryRestaurant)
    class Meta:
        db_table = u'restaurant_has_category'


    
class RestaurantHasTag(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    tag = models.ForeignKey(TagRestaurant)
    class Meta:
        db_table = u'restaurant_has_tag'
'''

class OrderStatus:
    CREATED = 1
    CONFIRMED = 2
    PAIED = 3
    COMPLETED = 4
    
