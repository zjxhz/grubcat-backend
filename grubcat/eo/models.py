# coding=utf-8
from datetime import datetime
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from django.db.models.query_utils import Q
from django.db.models.signals import post_save
from image_cropping.fields import ImageRatioField, ImageCropField
import random

# Create your models here.
from eo.exceptions import NoAvailableSeatsError, AlreadyJoinedError

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
    user = models.OneToOneField(User, null=True, related_name="restaurant")
    name = models.CharField(max_length=135)
    address = models.CharField(max_length=765)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
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
        verbose_name = u'餐厅'
        verbose_name_plural = u'餐厅'


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
    restaurant = models.ForeignKey(Restaurant)
    photo = models.FileField(u'图片', null=True, upload_to='uploaded_images/%Y/%m/%d')
    num_persons = models.SmallIntegerField(u'人数')
    average_price = models.DecimalField(u'均价',max_digits=8,decimal_places=1)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = u'menu'

class MenuItem(models.Model):
    '''
    菜单的项，可能是菜有可能是分类
    '''
    menu = models.ForeignKey(Menu,related_name='items')
    #use generic relation to respresent dish or category foreign keys
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = generic.GenericForeignKey()
    num = models.SmallIntegerField(u'份数',default=0)



class DishCategory(models.Model):
#    menu = models.ForeignKey(Menu, related_name="categories")
    name = models.CharField(u'菜名',max_length=45,unique=True)
#    if restaurant is null,it means the category is public, all restaurant can see the category
    restaurant = models.ForeignKey(Restaurant, verbose_name=u'餐厅', null=True, blank=True )
    #    parent_category = models.ForeignKey('self', null=True) #not used temporary

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = u'dish_category'
        verbose_name = u'菜的分类'
        verbose_name_plural = u'菜的分类'


class Dish(models.Model):
    name = models.CharField(u'菜名', max_length=135)
    price = models.DecimalField(u'价钱', decimal_places=2, max_digits=6)
    restaurant = models.ForeignKey(Restaurant, verbose_name=u'餐厅', )
    desc = models.CharField(u'描述',max_length=765,blank=True)
    #    pic = models.CharField(u'图片', max_length=765, blank=True)
    #    ingredient = models.CharField(u'原料',max_length=765, blank=True)
    #    cooking = models.CharField(u'烹饪做法',max_length=765, blank=True)
    #    taste = models.CharField(u'口味',max_length=18)
    #    is_mandatory = models.BooleanField(default=False)
    #    is_recommended = models.BooleanField(u'是否推荐菜', default=False)
    unit = models.CharField(u'单位', max_length=30, default=u'份')
    available = models.BooleanField(u'目前是否可以提供', default=True)
    categories = models.ManyToManyField(DishCategory,verbose_name=u'分类' )

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = u'dish'
        verbose_name = u'菜'
        verbose_name_plural = u'菜'


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

class OrderStatus():
    CREATED=1
    PAYIED=2
    USED=3
    CANCELED=4


ORDER_STATUS = (
    (1, '已创建'),
    (2, '已支付'),
    (3, '已使用'),
    (4, '已取消')
    )


class Order(models.Model):
    customer = models.ForeignKey('UserProfile', related_name='orders', verbose_name=u'客户')
    meal = models.ForeignKey('Meal', related_name='orders', verbose_name='饭局')
    num_persons = models.IntegerField(u"人数")
    status = models.IntegerField(u'订单状态', choices=ORDER_STATUS, default=1)
    total_price = models.DecimalField(u'总价钱', max_digits=6, decimal_places=2)
    created_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    paid_time = models.DateTimeField(u'支付时间', blank=True, null=True)
    completed_time = models.DateTimeField(u'就餐时间', blank=True, null=True)
    code  = models.CharField(u'订单验证码',max_length = 12, null=True, unique=True)

    @models.permalink
    def get_absolute_url(self):
        return 'order_detail', [str(self.meal_id), str(self.id)]

    def __unicode__(self):
        return "%s %s" % (self.meal.topic, self.customer.user.username)


    def save(self, *args, **kargs):
        if not self.code:
            self.gen_code()
        super(Order, self).save(*args, **kargs)

#    @transaction.commit_on_success
    def cancel(self):
        if self.status != OrderStatus.CANCELED:
            self.meal.participants.remove(self.customer)
            self.meal.actual_persons -= self.num_persons
            self.meal.save()
            self.status=OrderStatus.CANCELED
            self.save()

    def is_used(self):
        return self.status == OrderStatus.USED

    def get_random_code(self):
        return random.randint(10000000,99999999)

    def gen_code(self):
        r = self.get_random_code()
        while Order.objects.filter(code=str(r)).count() > 0:
            r = self.get_random_code()
        self.code = str(r)

    class Meta:
        db_table = u'order'
        verbose_name = u'订单'
        verbose_name_plural = u'订单'


class MealDishes(models.Model):
    meal = models.ForeignKey('Meal')
    dish = models.ForeignKey(Dish)
    quantity = models.FloatField()

    class Meta:
        db_table = u'meal_dishes'


class Relationship(models.Model):
    from_person = models.ForeignKey("UserProfile", related_name='from_user')
    to_person = models.ForeignKey("UserProfile", related_name='to_user')
    status = models.IntegerField(default=0) # FOLLOWING, BLOCKED

    def __unicode__(self):
        return '%s -> %s: %s' % (self.from_person, self.to_person, self.status)

    class Meta:
        db_table = u'relationship'
        unique_together = ('from_person','to_person')


class UserLocation(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = u"user_location"


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=30, null=True)
    favorite_restaurants = models.ManyToManyField(Restaurant, db_table="favorite_restaurants",
        related_name="user_favorite")
    following = models.ManyToManyField('self', related_name="related_to", symmetrical=False, through="RelationShip")
    recommended_following = models.ManyToManyField('self', symmetrical=False, db_table="recommended_following")
    gender = models.IntegerField(null=True)
    avatar = models.ImageField(upload_to='uploaded_images/%Y/%m/%d', max_length=256) # photo
    location = models.ForeignKey(UserLocation, unique=True, null=True)
    constellation = models.IntegerField(null=True, default=-1)
    birthday = models.DateTimeField(null=True)
    college = models.CharField(max_length=64, null=True)
    work_for = models.CharField(max_length=64, null=True)
    occupation = models.CharField(max_length=64, null=True)
    motto = models.CharField(max_length=140, null=True)
    weibo_id = models.CharField(max_length=20, null=True)
    weibo_access_token = models.CharField(max_length=128, null=True)

    @property
    def followers(self):
        return self.related_to.all()

    @property
    def meals(self):
        return Meal.objects.filter(Q(host=self) | Q(participants=self))
    
    @property
    def feeds(self):
        """
        orders that the followings create
        """
        return Order.objects.filter(customer__in=self.following.all())
        
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
    restaurant = models.ForeignKey(Restaurant, verbose_name=u'餐厅')
    dishes = models.ManyToManyField(Dish, through='MealDishes')
    topic = models.CharField(u'主题', max_length=64)
    introduction = models.CharField(u'简介', max_length=1024)
    list_price = models.DecimalField(u'价钱', max_digits=6, decimal_places=2)
    photo = models.FileField(u'图片', null=True, upload_to='uploaded_images/%Y/%m/%d') #if none use menu's cover
    time = models.DateTimeField(u'时间', )
    host = models.ForeignKey(UserProfile, null=True, related_name="host_user", verbose_name=u'发起者', )
    participants = models.ManyToManyField(UserProfile, related_name="meals", verbose_name=u'参加者', blank=True, null=True)
    likes = models.ManyToManyField(UserProfile, related_name="liked_meals", verbose_name=u'喜欢该饭局的人', blank=True, null=True)
    actual_persons = models.IntegerField(u'实际参加人数', default=0)
    min_persons = models.IntegerField(u'最少参加人数', )
    max_persons = models.IntegerField(u'最多参加人数', default=0) # not used for now, min_persons = max_persons
    type = models.IntegerField(default=0) # THEMES, DATES
    privacy = models.IntegerField(default=0) # PUBLIC, PRIVATE, VISIBLE_TO_FOLLOWERS?

    @transaction.commit_on_success
    def join(self, order):
        if self.actual_persons + order.num_persons > self.max_persons:
            raise NoAvailableSeatsError
        if self.is_participant(order.customer):
            raise AlreadyJoinedError()
        self.participants.add(order.customer)
        self.actual_persons += order.num_persons
        self.save()
        order.save()

    def is_participant(self, user_profile):
        for participant in self.participants.all(): #TODO query the user by id to see the if the user exist
            if participant == user_profile:
                return True
        return False

    def liked(self, user_profile):
        for like in self.likes.all():
            if like == user_profile:
                return True
        return False

    @property
    def comments(self):
        return self.comments.all()

    @property
    def left_persons(self):
        return self.max_persons - self.actual_persons

    @models.permalink
    def get_absolute_url(self):
        return 'meal_detail', [str(self.id)]

    def __unicode__(self):
        return self.topic

    class Meta:
        db_table = u'meal'
        verbose_name = u'饭局'
        verbose_name_plural = u'饭局'


class MealComment(models.Model):
    meal = models.ForeignKey(Meal, related_name="comments")
    from_person = models.ForeignKey(UserProfile)
    comment = models.CharField(max_length=42)
    timestamp = models.DateTimeField(default=datetime.now())

    class  Meta:
        db_table = u'meal_comment'


class MealInvitation(models.Model):
    from_person = models.ForeignKey(UserProfile, related_name="invitation_from_user")
    to_person = models.ForeignKey(UserProfile, related_name='invitation_to_user')
    meal = models.ForeignKey(Meal)
    timestamp = models.DateTimeField(default=datetime.now())
    status = models.IntegerField(default=0) # PENDING, ACCEPTED, REJECTED

    def is_related(self, user_profile):
        return self.from_person == user_profile or self.to_person == user_profile

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