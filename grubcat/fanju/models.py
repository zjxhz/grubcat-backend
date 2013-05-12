# coding=utf-8
from datetime import datetime, date, timedelta
from datetime import time as dtime
import time
import threading
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.staticfiles.storage import staticfiles_storage
from django.db import models, IntegrityError
from django.db.models import Max
from django.db.models.fields.files import ImageField
from django.db.models.query_utils import Q
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from easy_thumbnails.files import get_thumbnailer
from fanju.exceptions import BusinessException, AlreadyJoinedError, \
    NoAvailableSeatsError
from fanju.util import pubsub
from image_cropping.fields import ImageRatioField
from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, Tag
import json
import os
import random
#import redis
# Create your models here.


class Privacy:
    PUBLIC = 0
    PRIVATE = 1


class Region(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return u'%s' % self.name


class Restaurant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=u'用户', null=True, related_name="restaurant")
    name = models.CharField(u'餐厅名称', max_length=135)
    address = models.CharField(u'餐厅地址', max_length=765)
    longitude = models.FloatField(u'经度', null=True, blank=True)
    latitude = models.FloatField(u'纬度', null=True, blank=True)
    tel = models.CharField(u'电话', max_length=60, null=True, blank=True)
    introduction = models.CharField(u'简介', max_length=6000, blank=True)
    regions = models.ManyToManyField(Region, verbose_name=u'区域', null=True, blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.name, self.address)

    # def get_recommended_dishes(self, max_number=10):
    #     return BestRatingDish.objects.filter(restaurant__id=self.id).order_by('-times')[:max_number]

    # def get_rating(self):
    #     return Rating.objects.filter(restaurant__id=self.id)

    class Meta:
        verbose_name = u'餐厅'
        verbose_name_plural = u'餐厅'


class DishCategory(models.Model):
    name = models.CharField(u'菜名', max_length=45, )
    restaurant = models.ForeignKey(Restaurant, verbose_name=u'餐厅')

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        unique_together = ('name', 'restaurant')
        verbose_name = u'菜的分类'
        verbose_name_plural = u'菜的分类'


class Dish(models.Model):
    name = models.CharField(u'菜名', max_length=135)
    price = models.DecimalField(u'价钱', decimal_places=1, max_digits=6)
    restaurant = models.ForeignKey(Restaurant, verbose_name=u'餐厅', )
    desc = models.CharField(u'描述', max_length=765, blank=True)
    unit = models.CharField(u'单位', max_length=30, default=u'份')
    available = models.BooleanField(u'目前可以提供', default=True)
    categories = models.ManyToManyField(DishCategory, verbose_name=u'分类', blank=True)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
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
    name = models.CharField(u'套餐名称', max_length=40, blank=False, null=False)
    photo = models.ImageField(u'套餐封面', null=True, upload_to='uploaded_images/rest/%Y/%m/%d')
    cropping = ImageRatioField('photo', '420x280', adapt_rotation=False)
    num_persons = models.SmallIntegerField(u'就餐人数')
    average_price = models.DecimalField(u'人均消费', max_digits=6, decimal_places=1)
    created_time = models.DateTimeField(default=datetime.now())
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

    @property
    def big_cover_url(self):
        if self.photo:
            url = get_thumbnailer(self.photo).get_thumbnail({
                'size': (420, 280),
                'crop': True,
                'box': self.cropping,
                #                'quality':85,
                'detail': True,
            }).url
        else:
            url = staticfiles_storage.url("img/default/meal_cover.jpg")
        return url

    @property
    def normal_cover_url(self):
        if self.photo:
            url = get_thumbnailer(self.photo).get_thumbnail({
                'size': (360, 240),
                'crop': True,
                'box': self.cropping,
                #                'quality':85,
                'detail': True,
            }).url
        else:
            url = staticfiles_storage.url("img/default/meal_cover.jpg")
        return url

    @property
    def small_cover_url(self):
        if self.photo:
            url = get_thumbnailer(self.photo).get_thumbnail({
                'size': (150, 100),
                'crop': True,
                'box': self.cropping,
                #                'quality':85,
                'detail': True,
            }).url
        else:
            url = staticfiles_storage.url("img/default/meal_cover.jpg")
        return url


    def __unicode__(self):
        return u'套餐%s' % self.id

    class Meta:
        unique_together = (('restaurant', 'status', 'name'),)
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
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', verbose_name=u'客户')
    meal = models.ForeignKey('Meal', related_name='orders', verbose_name='饭局')
    num_persons = models.IntegerField(u"人数")
    status = models.IntegerField(u'订单状态', choices=ORDER_STATUS, default=1)
    total_price = models.DecimalField(u'总价钱', max_digits=6, decimal_places=2)
    created_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    payed_time = models.DateTimeField(u'支付时间', blank=True, null=True)
    completed_time = models.DateTimeField(u'就餐时间', blank=True, null=True)
    code = models.CharField(u'订单验证码',blank=True, max_length=12, null=True, unique=True)

    @models.permalink
    def get_absolute_url(self):
        return 'order_detail', [str(self.meal_id), str(self.id)]

    def __unicode__(self):
        return "%s: user%s attend meal%s" % (self.id, self.customer.id, self.meal.id)


    def set_payed(self):
        order = self
        order.status = OrderStatus.PAYIED
        # if payed_time:
        #     order.payed_time = payed_time
        if not order.code:
            order.gen_code()
        order.save()
        #set all other unpaid order as "canceld" status
        Order.objects.filter(meal=order.meal,customer=order.customer, status=OrderStatus.CREATED).update(status=OrderStatus.CANCELED)
        meal = order.meal
        MealParticipants.objects.create(meal=meal, user=order.customer)
        meal.actual_persons += order.num_persons
        if order.customer == meal.host:
            #创建饭局后，支付
            if meal.status is MealStatus.CREATED_NO_MENU:
                meal.status = MealStatus.PAID_NO_MENU
            elif meal.status is MealStatus.CREATED_WITH_MENU:
                meal.status = MealStatus.PUBLISHED
        meal.save()

    def cancel(self):
        if self.status != OrderStatus.CANCELED:
            MealParticipants.objects.filter(meal=self.meal, user=self.customer).delete()
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
        verbose_name = u'订单'
        verbose_name_plural = u'订单'

#交易流水
class TransFlow(models.Model):
    order = models.OneToOneField(Order, verbose_name=u'站内订单号', related_name='flow')
    alipay_trade_no = models.CharField(u'支付宝订单号', max_length=64)

    def __unicode__(self):
        return '%s' % self.alipay_trade_no

    class Meta:
        verbose_name = u'交易流水'
        verbose_name_plural = u'交易流水'


class Relationship(models.Model):
    from_person = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user')
    to_person = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user')
    status = models.IntegerField(default=0)  # FOLLOWING, BLOCKED

    def __unicode__(self):
        return u'%s -> %s: %s' % (self.from_person, self.to_person, self.status)

    class Meta:
        unique_together = ('from_person', 'to_person')
        verbose_name = u'用户关系'
        verbose_name_plural = u'用户关系'


class Visitor(models.Model):
    from_person = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="host")
    to_person = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="visitor")

    def __unicode__(self):
        return u'%s -> %s' % (self.from_person, self.to_person)

    class Meta:
        unique_together = ('from_person', 'to_person')
        verbose_name = u'用户访问'
        verbose_name_plural = u'用户访问'


class UserLocation(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    updated_at = models.DateTimeField()


class UserTag(Tag):
    image_url = models.ImageField(upload_to='uploaded_images/%Y/%m/%d', max_length=256) # background image

    def tagged_users(self):
        return [tagged_user.content_object for tagged_user in self.items.all()[:50] ]

    class Meta:
        verbose_name = u'兴趣标签'
        verbose_name_plural = u'兴趣标签'

class TaggedUser(GenericTaggedItemBase):
    tag = models.ForeignKey(UserTag, related_name='items')
    # related_name='items' is needed here or you can't get tags of User


class Gender:
    MALE = 0
    FEMALE = 1

GENDER_CHOICE = (
    (Gender.MALE, u'男'),
    (Gender.FEMALE, u'女'),
    )
INDUSTRY_CHOICE = (
    (0, u'计算机/互联网/通信'),
    (1, u'商业/服务业/个体经营'),
    (2, u'文化/广告/传媒'),
    (3, u'教师'),
    (4, u'医生'),
    (5, u'护士'),
    (6, u'空乘人员'),
    (7, u'生产/工艺/制造'),
    (8, u'商业/服务业/个体经营'),
    (9, u'金融/银行/投资/保险'),
    (10, u'娱乐/艺术/表演'),
    (11, u'律师/法务'),
    (12, u'教育/培训/管理咨询'),
    (13, u'建筑/房地产/物业'),
    (14, u'消费零售/贸易/交通物流'),
    (15, u'公务员/事业单位'),
    (16, u'酒店旅游'),
    (17, u'现代农业'),
    (18, u'在校学生'),
    )


class User(AbstractUser):
    name = models.CharField(u'昵称', max_length=30, null=True, blank=False)
    following = models.ManyToManyField('self', related_name="followers", symmetrical=False, through="RelationShip")
    visitoring = models.ManyToManyField('self', related_name="visitors", symmetrical=False, through="Visitor")
    gender = models.IntegerField(u'性别', null=True, choices=GENDER_CHOICE)
    avatar = models.ImageField(u'头像', upload_to='uploaded_images/%Y/%m/%d', max_length=256, blank=True, null=True) # photo
    cropping = ImageRatioField('avatar', '180x180', adapt_rotation=True)
    location = models.ForeignKey(UserLocation, unique=True, null=True, blank=True)
    constellation = models.IntegerField(u'星座', blank=True, null=True, default=-1)
    birthday = models.DateField(u'生日', null=True, blank=True)
    college = models.CharField(u'学校', max_length=64, null=True, blank=True)
    industry = models.SmallIntegerField(u'行业', null=True, blank=True, choices=INDUSTRY_CHOICE)
    work_for = models.CharField(u'公司', max_length=64, null=True, blank=True)
    occupation = models.CharField(u'职位', max_length=64, null=True, blank=True)
    motto = models.CharField(u'签名', max_length=140, null=True, blank=True)
    weibo_id = models.CharField(max_length=20, null=True, blank=True)
    weibo_access_token = models.CharField(max_length=128, null=True, blank=True)
    tags = TaggableManager(through=TaggedUser, blank=True)
    apns_token = models.CharField(max_length=255, blank=True)

    @models.permalink
    def get_absolute_url(self):
        return 'user_detail', [str(self.id)]
    
    def follow(self, followee):
        if self == followee:
            raise BusinessException(u'你不可以自己关注自己！')
        try:
            relationship = Relationship(from_person=self, to_person=followee)
            relationship.save()
        except IntegrityError:
            raise BusinessException(u'你已经关注了对方！')
    
    def is_following(self, another):
        if another.followers.filter(pk=self.pk):
            return True
        else:
            return False
        
    def get_passedd_orders(self):
        return self.orders.filter(status__in=(OrderStatus.PAYIED, OrderStatus.USED)).filter(
            Q(meal__start_date__lt=date.today()) | Q(meal__start_date=date.today(),
                                                     meal__start_time__lt=datetime.now().time())).order_by(
            "meal__start_date", "meal__start_time").select_related('meal')

    def get_upcomming_orders(self):
        return self.orders.filter(status=OrderStatus.PAYIED).filter(
            Q(meal__start_date__gt=date.today()) | Q(meal__start_date=date.today(),
                                                     meal__start_time__gt=datetime.now().time())).order_by(
            "meal__start_date", "meal__start_time").select_related('meal')

    #return 30分钟内未支付的饭局订单，如果一个饭局有多个未支付的订单，那么这个饭局只返回最新的一个订单
    def get_paying_orders(self):
        return self.orders.filter(id__in=[o['latest_order_id'] for o in self.__get_paying_order_ids()]).order_by(
            "meal__start_date", "meal__start_time").select_related('meal')

    #return 30分钟内未支付的饭局订单数，如果一个饭局有多个未支付的订单，那么这个饭局只返回最新的一个订单
    def get_paying_orders_count(self):
        return len(self.__get_paying_order_ids())

    #@return 30分钟内未支付的饭局订单的id，如果一个饭局有多个未支付的订单，那么这个饭局只返回最新的一个订单
    def __get_paying_order_ids(self):
        payed_orders = self.orders.filter(status=OrderStatus.PAYIED)
        all_paying_orders = self.orders.filter(status=OrderStatus.CREATED,
                                               created_time__gte=datetime.now() - timedelta(
                                                   minutes=settings.PAY_OVERTIME)).exclude(id__in=payed_orders)
        paying_orders_per_meal = all_paying_orders.values('meal').annotate(latest_order_id=Max('id'))
        return paying_orders_per_meal


    
    def avatar_thumbnailer(self, avatar_size):
        try:
            if self.avatar and os.path.exists(self.avatar.path):
                return get_thumbnailer(self.avatar).get_thumbnail({
                    'size': avatar_size,
                    'box': self.cropping,
                    'quality': 90,
                    'crop': True,
                    'detail': True,
                })
        except Exception:
            pass

    def avatar_thumbnail(self, width, height):
        return self.avatar_thumbnail_for_size((width, height))
            
    @property
    def age(self):
        if self.birthday:
            return date.today().year - self.birthday.year
        else:
            return None

    def avatar_thumbnail_for_size(self, size):
        if self.avatar and os.path.exists(self.avatar.path) and self.avatar_thumbnailer(size):
            return self.avatar_thumbnailer(size).url
        else:
            return staticfiles_storage.url("img/default/big_avatar.png")
        
    @property
    def big_avatar(self):
        return self.avatar_thumbnail_for_size(settings.BIG_AVATAR_SIZE)

    @property
    def normal_avatar(self):
        return self.avatar_thumbnail_for_size(settings.NORMAL_AVATAR_SIZE)

    @property
    def small_avatar(self):
        return self.avatar_thumbnail_for_size(settings.SMALL_AVATAR_SIZE)        
    
    @property
    def small_avatar_path(self):
        if self.avatar and os.path.exists(self.avatar.path) and self.avatar_thumbnailer(settings.SMALL_AVATAR_SIZE):
            return self.avatar_thumbnailer(settings.SMALL_AVATAR_SIZE).path
        else:
            return None

    #    To Be Deleted, checked in group pages
    @property
    def avatar_default_if_none(self):
        if self.avatar:
            return self.avatar.url
        else:
            return settings.MEDIA_URL + "uploaded_images/anno.png"

    @property
    def followers(self):
        return self.followers.all()

    @property
    def upcoming_meals(self):
        return Meal.objects.filter(Q(host=self) | Q(participants=self)).filter(
            Q(start_date__gt=date.today()) | 
            Q(start_date=date.today(), start_time__gt=datetime.now().time())).order_by(
            "start_date", "start_time")

    @property
    def feeds(self):
        """
        orders that the followings create
        """
        return Order.objects.filter(customer__in=self.following.all())

    # @property
    # def invitations(self):
    #     """ Invitation sent from others.
    #     """
    #     return MealInvitation.objects.filter(to_person=self).filter(status=0)

    @property
    def recommendations(self):
        """
        recommendations based on interests, people with more same interests will be listed first, other people
        who don't have same interests will be listed as well, users that this user has been already following will
        be excluded
        """
        return self.tags.similar_objects()

    # return a list of values with the order how keys are sorted for a given dict
    def sortedDictValues(self, some_dict):
        from operator import itemgetter

        sortedItems = sorted(some_dict.items(), key=itemgetter(1))
        return [key[0] for key in sortedItems]

    @property
    def non_restaurant_usres(self):
        return User.objects.exclude(user__restaurant__isnull=False)

    def users_nearby(self, lat=None, lng=None):
        distance_user_dict = {}
        if lat and lng:
            lat = float(lat)
            lng = float(lng)
        else:
            lat = self.location.lat
            lng = self.location.lng
        if not lat or not lng:
            return []
        for user in self.non_restaurant_usres.exclude(pk=self.id): #.exclude(pk__in=self.following.values('id')):
            if user.location:
                distance = self.getDistance(lng, lat, user.location.lng, user.location.lat)
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
        return\
        self.messages.filter(type=0).filter(Q(from_person=other_user) | Q(to_person=other_user)).order_by('timestamp')[
        :limit]

    def new_messages(self, last_message_id):
        last_message = UserMessage.objects.get(pk=last_message_id)
        return UserMessage.objects.filter(from_person=last_message.from_person).filter(
            timestamp__gt=last_message.timestamp).filter(type=0).order_by('timestamp')

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
        return self.name if self.name is not None else self.username

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = u'用户'


class UserPhoto(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="photos")
    photo = models.ImageField(upload_to='uploaded_images/%Y/%m/%d', max_length=256)

    def __unicode__(self):
        return str(self.id)

    @property
    def photo_thumbnail(self):
        try:
            return get_thumbnailer(self.photo).get_thumbnail({'size': (210, 210),
                                                              'crop': True,
                                                              'detail': True
            }).url
        except Exception:
            return None

    @property
    def large_photo(self):
        try:
            return get_thumbnailer(self.photo).get_thumbnail({'size': (700, 1400 ),
                                                              'crop': False,
                                                              'detail': True
                                                              }).url
        except Exception:
            return None
        
    @models.permalink
    def get_absolute_url(self):
        return 'photo_detail', [str(self.id)]

    class Meta:
        verbose_name = u'用户照片'
        verbose_name_plural = u'用户照片'


class UserMessage(models.Model):
    from_person = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_from_user")
    to_person = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_to_user')
    message = models.CharField(max_length=1024)
    timestamp = models.DateTimeField()
    type = models.IntegerField(default=0) # 0 message, 1 comments

    def __unicode__(self):
        return "%s -> %s(%s): %s" % (self.from_person, self.to_person, self.timestamp, self.message)


class MealPrivacy(Privacy):
    pass


MEAL_PRIVACY_CHOICE = (
    (MealPrivacy.PUBLIC, u"公开：所有人都可以参加"),
    (MealPrivacy.PRIVATE, u"私密：仅被邀请的人可以参加")
    )

MEAL_PERSON_CHOICE = [(x, "%s 人" % x) for x in range(2, 13)]
START_TIME_CHOICE = (
    (dtime(9, 00), "9:00"), (dtime(9, 30), "9:30"), (dtime(10, 00), "10:00"), (dtime(10, 30), "10:30"),
    (dtime(11, 00), "11:00"), (dtime(11, 30), "11:30"), (dtime(12, 00), "12:00"), (dtime(12, 30), "12:30"),
    (dtime(13, 00), "13:00"), (dtime(13, 30), "13:30"), (dtime(14, 00), "14:00"), (dtime(14, 30), "14:30"),
    (dtime(15, 00), "15:00"), (dtime(15, 30), "15:30"), (dtime(16, 00), "16:00"), (dtime(16, 30), "16:30"),
    (dtime(17, 00), "17:00"), (dtime(17, 30), "17:30"), (dtime(18, 00), "18:00"), (dtime(18, 30), "18:30"),
    (dtime(19, 00), "19:00"), (dtime(19, 30), "19:30"), (dtime(20, 00), "20:00"), (dtime(20, 30), "20:30"),
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
    start_time = models.TimeField(u'开始时间', choices=START_TIME_CHOICE, default=dtime(19, 00))
    # group = models.ForeignKey('Group', verbose_name=u'通知圈子', null=True, blank=True)
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
    host = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="host_user", verbose_name=u'发起者', )
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="meals", verbose_name=u'参加者', blank=True, null=True,
                                          through="MealParticipants")
    # likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_meals", verbose_name=u'喜欢该饭局的人', blank=True,
    #                                null=True)
    actual_persons = models.IntegerField(u'实际参加人数', default=0)
    type = models.IntegerField(default=0) # THEMES, DATES

    @classmethod
    def get_default_upcomming_meals(cls):
        return cls.objects.filter(status=MealStatus.PUBLISHED, privacy=MealPrivacy.PUBLIC).filter(
            Q(start_date__gt=date.today()) | Q(start_date=date.today(),
                start_time__gt=datetime.now().time())).order_by("start_date",
            "start_time").select_related("menu")

    def checkAvaliableSeats(self, customer, requesting_persons):
        other_paying_orders = self.orders.exclude(customer=customer).exclude(
            customer__in=self.participants.all()).filter(status=OrderStatus.CREATED,
                                                         created_time__gte=datetime.now() - timedelta(
                                                             minutes=settings.PAY_OVERTIME)).select_for_update().values(
            'customer').annotate(max_num_persons=Max('num_persons'))
        paying_persons = sum([o['max_num_persons'] for o in other_paying_orders])
        if self.actual_persons + requesting_persons + paying_persons > self.max_persons:
            if self.actual_persons >= self.max_persons:
                message = u'该饭局已卖光了！'
            elif paying_persons == 0:
                message = u'最多只可以预定%s个座位！' % (self.max_persons - self.actual_persons)
            elif requesting_persons > self.max_persons - self.actual_persons - paying_persons > 0:
                message = u'现在有%s位用户正在支付，最多只可以预定%s个座位，你可以%s分钟后再尝试预定！' % (
                    paying_persons, self.max_persons - self.actual_persons - paying_persons, settings.PAY_OVERTIME_FOR_PAY_OR_USER)
            else:
                message = u'现在有%s位用户正在支付，你可以%s分钟后再尝试预定！' % (paying_persons, settings.PAY_OVERTIME_FOR_PAY_OR_USER)
            raise NoAvailableSeatsError(message)

    def join(self, customer, requesting_persons):
        if self.is_participant(customer):
            raise AlreadyJoinedError(u"对不起，您已经加入了这个饭局，您可以加入其他感兴趣的饭局！")

        self.checkAvaliableSeats(customer, requesting_persons)

        order = Order()
        order.meal = self
        order.customer = customer
        order.num_persons = requesting_persons
        order.total_price = self.list_price * requesting_persons
        order.status = OrderStatus.CREATED
        order.save()
        return order

    @property
    def is_passed(self):
        return self.start_date < date.today() or (
            self.start_date == date.today() and self.start_time < datetime.now().time())

    def is_participant(self, user):
        return self.participants.filter(pk=user.id).exists()

    @property
    def comments(self):
        return self.comments.all()

    @property
    def left_persons(self):
        return self.max_persons - self.actual_persons

    @property
    def big_cover_url(self):
        if self.photo:
            url = get_thumbnailer(self.photo).get_thumbnail({
                'size': (420, 280),
                'crop': True,
                #                'quality':85,
                'detail': True,
            }).url
        else:
            url = self.menu.big_cover_url
        return url

    @property
    def normal_cover_url(self):
        if self.photo:
            url = get_thumbnailer(self.photo).get_thumbnail({
                'size': (360, 240),
                'crop': True,
                #                'box': self.cropping,
                #                'quality':85,
                'detail': True,
            }).url
        else:
            url = self.menu.normal_cover_url
        return url

    @property
    def small_cover_url(self):
        if self.photo:
            url = get_thumbnailer(self.photo).get_thumbnail({
                'size': (150, 100),
                'crop': True,
                #                'box': self.cropping,
                #                'quality':85,
                'detail': True,
            }).url
        else:
            url = self.menu.small_cover_url
        return url

    @models.permalink
    def get_absolute_url(self):
        return 'meal_detail', [str(self.id)]

    def __unicode__(self):
        return self.topic

    class Meta:
        verbose_name = u'饭局'
        verbose_name_plural = u'饭局'


class MealParticipants(models.Model):
    meal = models.ForeignKey(Meal)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    
    def __unicode__(self):
        return u"%s参加了饭局%s" %(self.user, self.meal)
        
    class Meta:
        ordering = ['id',]
        verbose_name = u'饭局参加者'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    from_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', blank=True)
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


class MealComment(Comment):
    meal = models.ForeignKey(Meal, related_name="comments")



# class ImageTest(models.Model):
#     image = ImageField(blank=True, null=True, upload_to='apps')
#     # size is "width x height"
#     cropping = ImageRatioField('image', '640x640')

####################################################  POST SAVE   #######################################
def _pubsub_user_created(instance):
    user = instance
    cl, jid = pubsub.create_client(user)
    node_name = "/user/%d/followers" % user.id
    pubsub.createNode(user, node_name, client=cl)
    node_name = "/user/%d/meals" % user.id
    pubsub.createNode(user, node_name, client=cl)
    pubsub.unsubscribe(user, node_name,
                       client=cl) # the user himself doesn't want to be bothered if he uploaded a photo
    node_name = "/user/%d/visitors" % user.id
    pubsub.createNode(user, node_name, client=cl)
    node_name = "/user/%d/photos" % user.id
    pubsub.createNode(user, node_name, client=cl)
    pubsub.unsubscribe(user, node_name,
                       client=cl) # the user himself doesn't want to be bothered if he uploaded a photo
    cl.disconnect()


def pubsub_user_created(sender, instance, created, **kwargs):
    if created:
        t = threading.Thread(target=_pubsub_user_created, args=(instance,))
        t.start()

post_save.connect(pubsub_user_created, sender=User, dispatch_uid="pubsub_user_created") #dispatch_uid is used here to make it not called more than once


def user_followed(sender, instance, created, **kwargs):
    if created:
        followee = instance.to_person
        follower = instance.from_person
        event = u'关注了你'

        pubsub.publish(followee, "/user/%d/followers" % followee.id, json.dumps({"follower": follower.id,
                                                                                 "message": u"%s%s" % (
                                                                                 follower.name, event),
                                                                                 "event": event,
                                                                                 "avatar": follower.normal_avatar,
                                                                                 "s_avatar": follower.small_avatar,
                                                                                 "name": follower.name,
        }))

        cl, jid = pubsub.create_client(follower)
        pubsub.subscribe(follower, "/user/%d/meals" % followee.id, client=cl)
        pubsub.subscribe(follower, "/user/%d/photos" % followee.id, client=cl)
        cl.disconnect()
post_save.connect(user_followed, sender=Relationship, dispatch_uid="user_followed")


def user_unfollowed(sender, instance, **kwargs):
    followee = instance.to_person
    follower = instance.from_person
    cl, jid = pubsub.create_client(follower)
    pubsub.unsubscribe(follower, "/user/%d/meals" % followee.id, client=cl)
    pubsub.unsubscribe(follower, "/user/%d/photos" % followee.id, client=cl)
    cl.disconnect()
    
post_delete.connect(user_unfollowed, sender=Relationship, dispatch_uid="user_unfollowed")

@receiver(post_save, sender=Meal, dispatch_uid="meal_created")
def meal_created(sender, instance, created, **kwargs):
    if created:
        meal = instance
        host = meal.host
        node_name = "/meal/%d/participants" % meal.id
        pubsub.createNode(host, node_name)


def _meal_joined(meal_participant):
    meal = meal_participant.meal
    joiner = meal_participant.user
    if meal.host and meal.host.id == joiner.id:
        event = u"发起了饭局"
    else:
        event = u"参加了饭局"
    payload = json.dumps({"meal": meal.id,
                          "participant": joiner.id,
                          "message": u"%s%s：%s" % (joiner.name, event, meal.topic),
                          "event": event,
                          "avatar": joiner.normal_avatar,
                          "s_avatar": joiner.small_avatar,
                          "name": joiner.name,
                          "topic": meal.topic,
                          "meal_photo": meal.small_cover_url})
    if not meal.host or meal.host.id != joiner.id:
        # host does not publish meal events to participants
        # and he has subscribed the events already when he created the meal
        meal_participant_node = "/meal/%d/participants" % meal.id
        pubsub.publish(meal.host, meal_participant_node, payload)
        pubsub.subscribe(joiner, meal_participant_node)
        #TODO how about quit the meal
    #remove the subscription for of the user who is the joiner of the meal
    # and is also the  follower of the joiner, to prevent duplicate notification'
    users_to_unsubscribe = meal.participants.filter(id__in=joiner.followers.all())
    followee_join_meal_node = "/user/%d/meals" % joiner.id
    for user in users_to_unsubscribe:
        pubsub.unsubscribe(user, followee_join_meal_node)
    time.sleep(1)
    pubsub.publish(joiner, followee_join_meal_node, payload)
    for user in users_to_unsubscribe:
        pubsub.subscribe(user, followee_join_meal_node)


@receiver(post_save, sender=MealParticipants, dispatch_uid="meal_joined")
def meal_joined(sender, instance, created, **kwargs):
    if created:
        t = threading.Thread(target=_meal_joined, args=(instance,))
        t.start()

@receiver(post_save, sender=Visitor, dispatch_uid="user_visited")
def user_visited(sender, instance, created, **kwargs):
    if created:
        visitor = instance.from_person
        if visitor.id != instance.to_person.id:
            node_name = "/user/%d/visitors" % instance.to_person.id
            event = u"查看了你的个人资料"
            payload = json.dumps({"visitor":visitor.id, 
                                  "message":u"%s%s" % (visitor.name, event),
                                  "event": event,
                                  "avatar":visitor.normal_avatar,
                                  "s_avatar":visitor.small_avatar,
                                  "name": visitor.name,
                                  })
            pubsub.publish(instance.to_person, node_name, payload)

@receiver(post_save, sender=UserPhoto, dispatch_uid="photo_uploaded")
def photo_uploaded(sender, instance, created, **kwargs):
    if created:
        node_name = "/user/%d/photos" % instance.user.id
        event = u"上传了一张照片"
        payload = json.dumps({"user":instance.user.id, 
                              "photo_id":instance.id, 
                              "photo_url":instance.photo.url,
                              "message":u"%s%s" % (instance.user.name, event),
                              "event": event,
                              "avatar":instance.user.normal_avatar,
                              "s_avatar":instance.user.small_avatar,
                              "name": instance.user.name,
                              "photo":instance.photo_thumbnail})
        pubsub.publish(instance.user, node_name, payload)