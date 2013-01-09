# coding=utf-8
from datetime import datetime, time, date
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.fields.files import ImageField
from django.db.models.query_utils import Q
from django.db.models.signals import post_save
from eo.exceptions import NoAvailableSeatsError, AlreadyJoinedError
from image_cropping.fields import ImageRatioField, ImageCropField
from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, Tag
import random
from datetime import timedelta
from easy_thumbnails.files import get_thumbnailer
#import redis
import os
# Create your models here.


class Privacy:
    PUBLIC = 0
    PRIVATE = 1


class Company(models.Model):
    name = models.CharField(max_length=135)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = u'company'


class RestaurantTag(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = u'restaurant_tag'

    def __unicode__(self):
        return u'%s' % self.name


class Region(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = u'region'


class Restaurant(models.Model):
    user = models.OneToOneField(User, null=True, related_name="restaurant")
    name = models.CharField(max_length=135)
    address = models.CharField(max_length=765)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
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


class DishCategory(models.Model):
#    menu = models.ForeignKey(Menu, related_name="categories")
#    TODO unique for restaurant and name
    name = models.CharField(u'菜名', max_length=45, )
    #    if restaurant is null,it means the category is public, all restaurant can see the category
    restaurant = models.ForeignKey(Restaurant, verbose_name=u'餐厅', null=True, blank=True)
    #    parent_category = models.ForeignKey('self', null=True) #not used temporary

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = u'dish_category'
        verbose_name = u'菜的分类'
        verbose_name_plural = u'菜的分类'


class Dish(models.Model):
    name = models.CharField(u'菜名', max_length=135)
    price = models.DecimalField(u'价钱', decimal_places=1, max_digits=6)
    restaurant = models.ForeignKey(Restaurant, verbose_name=u'餐厅', )
    desc = models.CharField(u'描述', max_length=765, blank=True)
    #    pic = models.CharField(u'图片', max_length=765, blank=True)
    #    ingredient = models.CharField(u'原料',max_length=765, blank=True)
    #    cooking = models.CharField(u'烹饪做法',max_length=765, blank=True)
    #    taste = models.CharField(u'口味',max_length=18)
    #    is_mandatory = models.BooleanField(default=False)
    #    is_recommended = models.BooleanField(u'是否推荐菜', default=False)
    unit = models.CharField(u'单位', max_length=30, default=u'份')
    available = models.BooleanField(u'目前可以提供', default=True)
    categories = models.ManyToManyField(DishCategory, verbose_name=u'分类')

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = u'dish'
        verbose_name = u'菜'
        verbose_name_plural = u'菜'


class MenuStatus:
    PUBLISHED = 0
    DELETED = 1

MENU_STATUS = (
    (MenuStatus.PUBLISHED, '已发布'),
    (MenuStatus.DELETED, '已删除')
    )

LIST_PRICE_CHOICE = [(x, "%s元/人" % int(x)) for x in (25.0, 30.0, 35.0, 40.0, 45.0)]

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    photo = models.FileField(u'图片', null=True, upload_to='uploaded_images/%Y/%m/%d')
    num_persons = models.SmallIntegerField(u'就餐人数')
    average_price = models.DecimalField(u'均价', max_digits=6, decimal_places=1, choices=LIST_PRICE_CHOICE)
    created_time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(u'状态', choices=MENU_STATUS, default=0)
    dish_items = models.ManyToManyField(Dish, through='DishItem')
    dish_category_items = models.ManyToManyField(DishCategory, through='DishCategoryItem')

    @property
    def items(self):
        #items(dish or category) sorted by the order no
        items = list(self.dishitem_set.all().prefetch_related('dish'))
        items.extend(list(self.dishcategoryitem_set.all().prefetch_related('category')))
        items.sort(key=lambda item: item.order_no)
        return items

    def __unicode__(self):
        return u'套餐%s' % self.id

    class Meta:
        db_table = u'menu'
        verbose_name = u'套餐'
        verbose_name_plural = u'套餐'


class DishItem(models.Model):
    menu = models.ForeignKey(Menu)
    dish = models.ForeignKey(Dish)
    num = models.SmallIntegerField()
    order_no = models.SmallIntegerField() #菜在一个Menu中的顺序


class DishCategoryItem(models.Model):
    menu = models.ForeignKey(Menu)
    category = models.ForeignKey(DishCategory)
    order_no = models.SmallIntegerField() #分类在一个Menu中的顺序

###    group related  ###
class GroupCategory(models.Model):
    name = models.CharField(u'圈子分类名', max_length=30, unique=True)
    cover = models.ImageField(u'分类图片', upload_to='category_cover', blank=True, null=True)

    @property
    def cover_url_default_if_none(self):
        if self.cover:
            return self.cover.url
        else:
            return settings.STATIC_URL + 'img/default/category-cover.png'

    def __unicode__(self):
        return  self.name

    class Meta:
        verbose_name = u'圈子分类'
        verbose_name_plural = u'圈子分类'


class GroupPrivacy(Privacy):
    pass

GROUP_PRIVACY_CHOICE = (
    (GroupPrivacy.PUBLIC, u'公开：所有人都可以加入'),
    (GroupPrivacy.PRIVATE, u'私密：仅被邀请的人可以加入')
    )

class Group(models.Model):
    """圈子"""
    name = models.CharField(u'名称', max_length=15, unique=True)
    desc = models.CharField(u'描述', max_length=100)
    category = models.ForeignKey(GroupCategory, verbose_name=u'分类', null=True, blank=True)
    privacy = models.SmallIntegerField(u'公开', choices=GROUP_PRIVACY_CHOICE, default=GroupPrivacy.PUBLIC)
    owner = models.ForeignKey(User, verbose_name=u'创建者')
    logo = models.ImageField(upload_to='group_logos', blank=True, null=True)
    members = models.ManyToManyField(User, verbose_name=u'成员', related_name='interest_groups')

    @property
    def recent_meals(self):
        return Meal.objects.filter(group=self).filter(
            Q(start_date__gt=datetime.today()) | Q(start_date=datetime.today(),
                start_time__gt=datetime.now())).order_by("start_date",
            "start_time")

    @property
    def passed_meals(self):
        return Meal.objects.filter(group=self).filter(
            Q(start_date__lt=datetime.today()) | Q(start_date=datetime.today(),
                start_time__lte=datetime.now())).order_by("start_date",
            "start_time")

    @property
    def logo_url_default_if_none(self):
        if self.logo:
            return self.logo.url
        else:
            return settings.STATIC_URL + 'img/default/group-logo.jpg'

    @models.permalink
    def get_absolute_url(self):
        return 'group_detail', (self.id, )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'圈子'
        verbose_name_plural = u'圈子'


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
    CREATED = 1
    PAYIED = 2
    USED = 3
    CANCELED = 4


ORDER_STATUS = (
    (OrderStatus.CREATED, '已创建'),
    (OrderStatus.PAYIED, '已支付'),
    (OrderStatus.USED, '已使用'),
    (OrderStatus.CANCELED, '已取消')
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
    code = models.CharField(u'订单验证码', max_length=12, null=True, unique=True)

    @models.permalink
    def get_absolute_url(self):
        return 'order_detail', [str(self.meal_id), str(self.id)]

    def __unicode__(self):
        return "%s %s" % (self.meal.topic, self.customer.user.username)


    def save(self, *args, **kargs):
        if not self.code:
            self.gen_code()
        super(Order, self).save(*args, **kargs)

    def cancel(self):
        if self.status != OrderStatus.CANCELED:
            self.meal.participants.remove(self.customer)
            self.meal.actual_persons -= self.num_persons
            self.meal.save()
            self.status = OrderStatus.CANCELED
            self.save()

    def is_used(self):
        return self.status == OrderStatus.USED

    def get_random_code(self):
        return random.randint(10000000, 99999999)

    def gen_code(self):
        r = self.get_random_code()
        while Order.objects.filter(code=str(r)).count() > 0:
            r = self.get_random_code()
        self.code = str(r)

    class Meta:
        db_table = u'order'
        verbose_name = u'订单'
        verbose_name_plural = u'订单'


class Relationship(models.Model):
    from_person = models.ForeignKey("UserProfile", related_name='from_user')
    to_person = models.ForeignKey("UserProfile", related_name='to_user')
    status = models.IntegerField(default=0) # FOLLOWING, BLOCKED

    def __unicode__(self):
        return '%s -> %s: %s' % (self.from_person, self.to_person, self.status)

    class Meta:
        db_table = u'relationship'
        unique_together = ('from_person', 'to_person')


class UserLocation(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = u"user_location"


class UserTag(Tag):
    image_url = models.ImageField(upload_to='uploaded_images/%Y/%m/%d', max_length=256) # background image

    class Meta:
        db_table = u'user_tag'


class TaggedUser(GenericTaggedItemBase):
    tag = models.ForeignKey(UserTag,
        related_name='items') # related_name='items' is needed here or you can't get tags of UserProfile

    class Meta:
        db_table = u'tagged_user'

class Gender:
    MALE=0
    FEMALE=1
GENDER_CHOICE=(
    (Gender.MALE, u'男'),
    (Gender.FEMALE, u'女'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=30, null=True,blank=False)
    favorite_restaurants = models.ManyToManyField(Restaurant, db_table="favorite_restaurants",  blank=True,
        related_name="user_favorite")
    following = models.ManyToManyField('self', related_name="related_to", symmetrical=False, through="RelationShip")
    recommended_following = models.ManyToManyField('self', symmetrical=False, db_table="recommended_following",blank=True,null=True)
    gender = models.IntegerField(blank=False, null=True,choices=GENDER_CHOICE)
    avatar = models.ImageField(upload_to='uploaded_images/%Y/%m/%d', max_length=256) # photo
    cropping = ImageRatioField('avatar', '640x640', adapt_rotation=True)
    location = models.ForeignKey(UserLocation, unique=True, null=True,blank=True)
    constellation = models.IntegerField(blank=True, null=True, default=-1)
    birthday = models.DateField(null=True,blank=False)
    college = models.CharField(max_length=64, null=True,blank=True)
    work_for = models.CharField(max_length=64, null=True,blank=True)
    occupation = models.CharField(max_length=64, null=True,blank=True)
    motto = models.CharField(max_length=140, null=True, blank=True)
    weibo_id = models.CharField(max_length=20, null=True,blank=True)
    weibo_access_token = models.CharField(max_length=128, null=True,blank=True)
    tags = TaggableManager(through=TaggedUser)
    apns_token = models.CharField(max_length=255, blank=True)
    
    def avatar_thumbnail(self, width, height):
        if self.avatar:
            return get_thumbnailer(self.avatar).get_thumbnail({'size': (width, height),
                                                               'box': self.cropping,
                                                               'crop': True,
                                                               'detail': True
            }).url
        else:
            return settings.MEDIA_URL + "uploaded_images/anno.png"

    def avatar_thumbnailer(self, avatar_size):
        return get_thumbnailer(self.avatar).get_thumbnail({
            'size': avatar_size,
            'box': self.cropping,
            'quality':100,
            'crop': True,
            'detail': True,
        })
        
    @property
    def big_avatar(self):
        if self.avatar and os.path.exists(self.avatar.path):
            thumbnail_url = self.avatar_thumbnailer(settings.BIG_AVATAR_SIZE).url
        else:
            thumbnail_url = settings.STATIC_URL + "img/default/big_avatar.png"
        return thumbnail_url

    @property
    def normal_avatar(self):
        if self.avatar and os.path.exists(self.avatar.path):
            thumbnail_url = self.avatar_thumbnailer(settings.NORMAL_AVATAR_SIZE).url
        else:
            thumbnail_url = settings.STATIC_URL + "img/default/normal_avatar.png"
        return thumbnail_url

    @property
    def small_avatar(self):
        if self.avatar and os.path.exists(self.avatar.path):
            thumbnail_url = self.avatar_thumbnailer(settings.SMALL_AVATAR_SIZE).url
        else:
            thumbnail_url = settings.STATIC_URL + "img/default/small_avatar.png"
        return thumbnail_url
    
    @property
    def small_avatar_path(self):
        if self.avatar and os.path.exists(self.avatar.path):
            thumbnail_url = self.avatar_thumbnailer(settings.SMALL_AVATAR_SIZE).path
        else:
            thumbnail_url = None
        return thumbnail_url

    #    To Be Deleted
    @property
    def avatar_default_if_none(self):
        if self.avatar:
            return self.avatar.url
        else:
            return settings.MEDIA_URL + "uploaded_images/anno.png"

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
    def recommendations(self):
        """
        recommendations based on interests, people with more same interests will be listed first, other people
        who don't have same interests will be listed as well, users that this user has been already following will
        be excluded
        """
        recommended_list = self.tags.similar_objects()
        recommended_not_following = [u for u in recommended_list if u not in self.following.all()]

        recommended_list_ids = [user.id for user in recommended_list]
        other_users = UserProfile.objects.exclude(pk__in=recommended_list_ids).exclude(pk=self.id)
        other_users_not_following = other_users.exclude(pk__in=self.following.values('id'))

        return recommended_not_following + list(other_users_not_following)

    # return a list of values with the order how keys are sorted for a given dict
    def sortedDictValues(self, some_dict):
        from operator import itemgetter

        sortedItems = sorted(some_dict.items(), key=itemgetter(1))
        return [key[0] for key in sortedItems]

    @property
    def users_nearby(self):
        distance_user_dict = {}
        for user in UserProfile.objects.exclude(pk=self.id): #.exclude(pk__in=self.following.values('id')):
            if user.faked_location.lat and user.faked_location.lng:
                distance = self.getDistance(self.faked_location.lng, self.faked_location.lat, user.faked_location.lng,
                    user.faked_location.lat)
                distance_user_dict[user] = distance
        return self.sortedDictValues(distance_user_dict)

    # get distance in meter, code from google maps
    def getDistance(self, lng1, lat1, lng2, lat2):
        EARTH_RADIUS = 6378.137
        from math import asin, sin, cos, radians, pow, sqrt

        radLat1 = radians(lat1)
        radLat2 = radians(lat2)
        a = radLat1 - radLat2
        b = radians(lng1) - radians(lng2)
        s = 2 * asin(sqrt(pow(sin(a / 2), 2) + cos(radLat1) * cos(radLat2) * pow(sin(b / 2), 2)))
        s = s * EARTH_RADIUS
        return s * 1000

    @property
    def faked_location(self):
        """
        Used for testing when user location is not available
        """
        if self.location:
            return self.location
        else:
            location = UserLocation()
            location.lat = 30.275
            location.lng = 120.148
            location.updated_at = datetime.now() - timedelta(minutes=random.randint(0, 60 * 24 * 30))
            self.location = location
    
            return location
    
    @property
    def messages(self):
        return UserMessage.objects.filter(Q(from_person=self) | Q(to_person=self))
    
    @property
    def received_comments(self):
        return UserMessage.objects.filter(to_person=self).filter(type=1)
    
    @property
    def latest_messages_by_user(self):
        dic = {}
        for message in self.messages.filter(type=0): #TODO order by time
            other_person = message.from_person 
            if other_person == self:
                other_person = message.to_person
            temp = dic.get(other_person)
            if temp and temp.timestamp > message.timestamp:
                continue
            else:
                dic[other_person] = message
        return dic.values()
    
    def chat_history_with_user(self, other_user, limit=20):
        return self.messages.filter(type=0).filter(Q(from_person=other_user) | Q(to_person=other_user) ).order_by('timestamp')[:limit]
    
    def new_messages(self, last_message_id):
        last_message = UserMessage.objects.get(pk=last_message_id)
        return UserMessage.objects.filter(from_person=last_message.from_person).filter(timestamp__gt=last_message.timestamp).filter(type=0).order_by('timestamp')

#    def talk_to(self, another, message):
#        r = redis.StrictRedis(host='localhost', port=6379, db=0)
#        mid = r.incr("global.message.id")
#        r.set("mid:%d:message" % mid, message)
#        r.set("mid:%d:from" % mid, self.id)
#        r.set("mid:%d:to" % mid, another.id)
#        r.set("mid:%d:time" % mid, datetime.now())
#        r.sadd("uid:%d:contacts" %  self.id, another.id)
#        r.sadd("uid:%d:contacts" %  another.id, self.id)
#        r.lpush("uid:%d:chat:%d" %  (self.id, another.id), mid)
#        r.lpush("uid:%d:chat:%d" %  (another.id, self.id), mid)
#    
#    def contacts(self):
#        r = redis.StrictRedis(host='localhost', port=6379, db=0)
#        response = []
#        for uid in r.smembers("uid:%d:contacts" % self.id):
#            message = {}
#            mid = int(r.lrange("uid:%d:chat:%s" % (self.id, uid), 0, 1)[0])
#            message["from_person"] = r.get("mid:%d:from" % mid)
#            message["to_person"] = r.get("mid:%d:to" % mid)
#            message["time"] = r.get("mid:%d:time" % mid)
#            message["message"] = r.get("mid:%d:message" % mid)
#            response.append(message)
#        print response
                             
    def __unicode__(self):
        return self.user.username

    class Meta:
        db_table = u'user_profile'
        verbose_name = u'用户资料'
        verbose_name_plural = u'用户资料'


class UserPhoto(models.Model):
    user = models.ForeignKey(UserProfile, related_name="photos")
    photo = models.ImageField(upload_to='uploaded_images/%Y/%m/%d', max_length=256)

    class Meta:
        db_table = u'user_photo'


class UserMessage(models.Model):
    from_person = models.ForeignKey(UserProfile, related_name="sent_from_user")
    to_person = models.ForeignKey(UserProfile, related_name='sent_to_user')
    message = models.CharField(max_length=1024)
    timestamp = models.DateTimeField()
    type = models.IntegerField(default=0) # 0 message, 1 comments

    class Meta:
        db_table = u'user_message'
    
    def __unicode__(self):
        return "%s -> %s(%s): %s" % (self.from_person, self.to_person, self.timestamp, self.message)

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

#meal related choice
class MealPrivacy(Privacy):
    pass

MEAL_PRIVACY_CHOICE = (
    (MealPrivacy.PUBLIC, u"公开：所有人都可以参加"),
    (MealPrivacy.PRIVATE, u"私密：仅被邀请的人可以参加")
    )

MEAL_PERSON_CHOICE = [(x, "%s 人" % x) for x in range(3, 13)]
START_TIME_CHOICE = (
    (time(9, 00), "9:00"), (time(9, 30), "9:30"), (time(10, 00), "10:00"), (time(10, 30), "10:30"),
    (time(11, 00), "11:00"), (time(11, 30), "11:30"), (time(12, 00), "12:00"), (time(12, 30), "12:30"),
    (time(13, 00), "13:00"), (time(13, 30), "13:30"), (time(14, 00), "14:00"), (time(14, 30), "14:30"),
    (time(15, 00), "15:00"), (time(15, 30), "15:30"), (time(16, 00), "16:00"), (time(16, 30), "16:30"),
    (time(17, 00), "17:00"), (time(17, 30), "17:30"), (time(18, 00), "18:00"), (time(18, 30), "18:30"),
    (time(19, 00), "19:00"), (time(19, 30), "19:30"), (time(20, 00), "20:00"), (time(20, 30), "20:30"),
    )

class MealStatus:
    CREATED_NO_MENU = 0
    CREATED_WITH_MENU = 1
    PAID_NO_MENU = 2
    PUBLISHED = 3 #

MEAL_STATUS_CHOICE = (
    (MealStatus.CREATED_NO_MENU, u'创建且无菜单' ),
    (MealStatus.CREATED_WITH_MENU, u'创建且有菜单'),
    (MealStatus.PAID_NO_MENU, u'支付且无菜单'),
    (MealStatus.PUBLISHED, u'可以发布')
    )

class Meal(models.Model):
    topic = models.CharField(u'主题', max_length=64)
    introduction = models.CharField(u'简介', max_length=1024)
    #    time = models.DateTimeField(u'开始时间', )
    start_date = models.DateField(u'开始日期', default=datetime.today())
    start_time = models.TimeField(u'开始时间', choices=START_TIME_CHOICE, default=time(19, 00))
    group = models.ForeignKey('Group', verbose_name=u'通知圈子', null=True, blank=True)
    privacy = models.IntegerField(u'是否公开', default=MealPrivacy.PUBLIC,
        choices=MEAL_PRIVACY_CHOICE) # PUBLIC, PRIVATE, VISIBLE_TO_FOLLOWERS?
    min_persons = models.IntegerField(u'参加人数', choices=MEAL_PERSON_CHOICE, default=8)
    region = models.ForeignKey(Region, verbose_name=u'区域', blank=True, null=True)
    list_price = models.DecimalField(u'均价', max_digits=6, decimal_places=1, choices=LIST_PRICE_CHOICE, default=30.0,
        blank=True, null=True)
    extra_requests = models.CharField(u'其它要求', max_length=128, null=True, blank=True)
    status = models.SmallIntegerField(u'饭局状态', choices=MEAL_STATUS_CHOICE, default=MealStatus.CREATED_NO_MENU)
    max_persons = models.IntegerField(u'最多参加人数', default=0, blank=True, null=True) # not used for now,
    photo = models.FileField(u'图片', null=True, blank=True,
        upload_to='uploaded_images/%Y/%m/%d') #if none use menu's cover
    restaurant = models.ForeignKey(Restaurant, verbose_name=u'餐厅', blank=True, null=True) #TODO retrieve from menu
    menu = models.ForeignKey(Menu, verbose_name=u'菜单', null=True, blank=True)
    host = models.ForeignKey(UserProfile, null=True, blank=True, related_name="host_user", verbose_name=u'发起者', )
    participants = models.ManyToManyField(UserProfile, related_name="meals", verbose_name=u'参加者', blank=True, null=True)
    likes = models.ManyToManyField(UserProfile, related_name="liked_meals", verbose_name=u'喜欢该饭局的人', blank=True,
        null=True)
    actual_persons = models.IntegerField(u'实际参加人数', default=0)
    type = models.IntegerField(default=0) # THEMES, DATES

    def join(self, order):
        if self.actual_persons + order.num_persons > self.max_persons:
            raise NoAvailableSeatsError
        if self.is_participant(order.customer):
            raise AlreadyJoinedError()
        self.participants.add(order.customer)
        self.actual_persons += order.num_persons
        self.save()
        order.save()

    def is_reservable(self):
        return True

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

    def get_cover_url(self):
        if self.photo:
            url = get_thumbnailer(self.photo).get_thumbnail({
                'size':(420,280),
                'crop': True,
#                'quality':85,
                'detail': True,
                }).url
        else:
            url = settings.STATIC_URL + "img/default/meal_cover.jpg"
        return url

    def get_small_cover_url(self):
        if self.photo:
            url = get_thumbnailer(self.photo).get_thumbnail({
                'size':(360,240),
                'crop': True,
                #                'quality':85,
                'detail': True,
                }).url
        else:
            url = settings.STATIC_URL + "img/default/meal_cover.jpg"
        return url

    @models.permalink
    def get_absolute_url(self):
        return 'meal_detail', [str(self.id)]

    def __unicode__(self):
        return self.topic

    class Meta:
        db_table = u'meal'
        verbose_name = u'饭局'
        verbose_name_plural = u'饭局'


class Comment(models.Model):
    from_person = models.ForeignKey(UserProfile, verbose_name='作者', blank=True)
    comment = models.CharField(u'评论', max_length=300)
    timestamp = models.DateTimeField(blank=True, auto_now_add=True)

    @property
    def time_gap(self):
        gap = datetime.now() - self.timestamp
        if gap.days >= 365:
            result = u"%d年前" % (gap.days / 365)
        elif gap.days >= 31:
            result = u"%d个月前" % (gap.days / 31)
        elif gap.days > 0:
            result = u"%d天前" % gap.days
        elif gap.seconds >= 3600:
            result = u"%d小时前" % (gap.seconds / 3600)
        elif gap.seconds >= 60:
            result = u"%d分钟前" % (gap.seconds / 60)
        else:
            result = u"1分钟内"
        return result

    class Meta:
        abstract = True


class GroupComment(Comment):
    group = models.ForeignKey(Group, verbose_name=u'圈子', related_name='comments')
    parent = models.ForeignKey('self', related_name='replies', verbose_name=u'父评论', null=True, blank=True)

    class Meta:
        verbose_name = u'圈子评论'
        verbose_name_plural = u'圈子评论'

    def __unicode__(self):
        return  u'圈子(%s) 评论%s' % (self.group, self.id)


class MealComment(Comment):
    meal = models.ForeignKey(Meal, related_name="comments")

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
    image = ImageField(blank=True, null=True, upload_to='apps')
    # size is "width x height"
    cropping = ImageRatioField('image', '640x640')
