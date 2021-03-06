# coding=utf-8
from datetime import datetime, date, timedelta
from datetime import time as dtime
import logging
import threading
import json
import random

from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy
from django.core.cache import cache
from django.db import models, IntegrityError
from django.db.models import Max
from django.db.models.query_utils import Q
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from easy_thumbnails.files import get_thumbnailer
from image_cropping.fields import ImageRatioField
from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, Tag
import weibo

from fanju.exceptions import BusinessException, AlreadyJoinedError, \
    NoAvailableSeatsError
from fanju.util import pubsub, get_unread_message_count, get_unread_noty_count


#import redis
# Create your models here.
logger = logging.getLogger(__name__)


class CacheKey:
    USER_TAG = "user_tags_%s"


class CacheUtil:
    @classmethod
    def get_user_tags(cls, user):
        user_tags = cache.get(CacheKey.USER_TAG % user.id)
        if user_tags is None:
            user_tags = [tag.name for tag in user.tags.all()]
            cache.set(CacheKey.USER_TAG % user.id, user_tags)
        return user_tags


class Privacy:
    PUBLIC = 0
    PRIVATE = 1


class AuditStatus:
    WAIT_TO_AUDIT = 0
    APPROVED = 1
    UNAPPROVED_BY_MACHINE = 2
    UNAPPROVED_BY_ADMIN = 3
    DELETED = 4


AUDIT_STATUS_CHOICE = (
    (AuditStatus.WAIT_TO_AUDIT, u'待审核'),
    (AuditStatus.APPROVED, u'人工审核通过'),
    (AuditStatus.UNAPPROVED_BY_ADMIN, u'人工审核不通过'),
    (AuditStatus.UNAPPROVED_BY_MACHINE, u'机器审核不通过'),
    (AuditStatus.DELETED, u'已删除'),
)


class UserStatus(AuditStatus):
    BLACKLIST = 5


USER_STATUS_CHOICE = AUDIT_STATUS_CHOICE + ( (UserStatus.BLACKLIST, u'黒名单'),)


class Region(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return u'%s' % self.name


class Restaurant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=u'用户', null=True, related_name="restaurant")
    name = models.CharField(u'餐厅名称', max_length=135)
    address = models.CharField(u'餐厅地址', max_length=765)
    longitude = models.FloatField(u'经度', null=True)
    latitude = models.FloatField(u'纬度', null=True)
    tel = models.CharField(u'电话', max_length=60, null=True, blank=True)
    introduction = models.CharField(u'简介', max_length=6000, blank=True)
    regions = models.ManyToManyField(Region, verbose_name=u'区域', null=True, blank=True)

    def __unicode__(self):
        return u'%s' % (self.name,)

    # def get_recommended_dishes(self, max_number=10):
    #     return BestRatingDish.objects.filter(restaurant__id=self.id).order_by('-times')[:max_number]

    # def get_rating(self):
    #     return Rating.objects.filter(restaurant__id=self.id)

    class Meta:
        verbose_name = u'餐厅'
        verbose_name_plural = u'餐厅'


class DishCategory(models.Model):
    name = models.CharField(u'分类', max_length=45, )
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
    unit = models.CharField(u'单位', max_length=30, default=u'份')
    desc = models.CharField(u'描述', max_length=765, blank=True)
    categories = models.ManyToManyField(DishCategory, verbose_name=u'分类', blank=True)
    restaurant = models.ForeignKey(Restaurant, verbose_name=u'餐厅', )
    available = models.BooleanField(u'目前可以提供', default=True)

    def unique_error_message(self, model_class, unique_check):
        return u'菜名重复，如果已经添加过这道菜，您可以选择编辑！'

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        unique_together = ('name', 'restaurant')
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

    def get_cover_thumbnail(self, size):
        return get_thumbnailer(self.photo).get_thumbnail({
            'size': size,
            'crop': True,
            'box': self.cropping,
        }).url

    @property
    def big_cover_url(self):
        return self.get_cover_thumbnail(settings.BIG_MENU_COVER_SIZE)

    @property
    def normal_cover_url(self):
        return self.get_cover_thumbnail(settings.NORMAL_MENU_COVER_SIZE)

    @property
    def normal_cover_path(self):
        return get_thumbnailer(self.photo).get_thumbnail({
            'size': settings.NORMAL_MENU_COVER_SIZE,
            'crop': True,
            'box': self.cropping,
        }).path

    @property
    def small_cover_url(self):
        return self.get_cover_thumbnail(settings.SMALL_MENU_COVER_SIZE)

    @property
    def mini_cover_url(self):
        return self.get_cover_thumbnail(settings.MINI_MENU_COVER_SIZE)

    def __unicode__(self):
        if self.status == MenuStatus.PUBLISHED:
            status = u'已发布'
        else:
            status = u'已删除'
        return u'(%s) %s %s %s (%s元)' % (status, str(self.id), self.restaurant.name, self.name, str(self.average_price))

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
    orginal_total_price = models.DecimalField(u'优惠前总价钱', max_digits=6, decimal_places=1)
    total_price = models.DecimalField(u'优惠后总价钱', max_digits=6, decimal_places=1)
    created_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    payed_time = models.DateTimeField(u'支付时间', blank=True, null=True)
    completed_time = models.DateTimeField(u'就餐时间', blank=True, null=True)
    code = models.CharField(u'订单验证码', blank=True, max_length=12, null=True, unique=True)

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
        Order.objects.filter(meal=order.meal, customer=order.customer, status=OrderStatus.CREATED).update(
            status=OrderStatus.CANCELED)
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
        order.customer.add_score(Score.JOIN_MEAL)
        from fanju import tasks

        tasks.share_meal.delay(order.customer.id, order.meal.id, is_join=True)

    def cancel(self):
        if self.status != OrderStatus.CANCELED:
            MealParticipants.objects.filter(meal=self.meal, user=self.customer).delete()
            self.meal.actual_persons -= self.num_persons
            self.meal.save()
            self.status = OrderStatus.CANCELED
            self.save()
            self.customer.minus_score(Score.JOIN_MEAL)

    def is_used(self):
        return self.status == OrderStatus.USED

    def guest_num(self):
        return self.num_persons - 1

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


class PhotoRequest(models.Model):
    from_person = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="photo_requesting")
    to_person = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="photo_requesters")

    def __unicode__(self):
        return u'%s -> %s' % (self.from_person, self.to_person)

    class Meta:
        unique_together = ('from_person', 'to_person')
        verbose_name = u'求照片'
        verbose_name_plural = u'求照片'


class UserLocation(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    updated_at = models.DateTimeField()

    def __unicode__(self):

        if self.lat == settings.FAKED_LAT and self.lng == settings.FAKED_LNG:
            return u'(%s) fake location'
        else:
            return u'%s, %s' % (self.lat, self.lng)


class UserTag(Tag):
    image_url = models.ImageField(upload_to='uploaded_images/%Y/%m/%d', max_length=256) # background image

    def tagged_users(self):
        return [tagged_user.content_object for tagged_user in self.items.all()[:50]]

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


class Score:
    JOIN_MEAL = 100
    UPLOAD_PHOTO = 10


class User(AbstractUser):
    name = models.CharField(u'昵称', max_length=30, null=True, blank=False)
    following = models.ManyToManyField('self', related_name="followers", symmetrical=False, through="RelationShip")
    visitoring = models.ManyToManyField('self', related_name="visitors", symmetrical=False, through="Visitor")
    gender = models.IntegerField(u'性别', null=True, choices=GENDER_CHOICE)
    avatar = models.ImageField(u'头像', upload_to='uploaded_images/%Y/%m/%d', max_length=256, blank=True,
                               null=True) # photo
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
    apns_token = models.CharField(max_length=255, blank=True, null=True)
    background_image = models.ImageField(u'背景图片', upload_to='uploaded_images/%Y/%m/%d', max_length=256, blank=True,
                                         null=True)
    mobile = models.CharField(u'手机号码', max_length=11, null=True, blank=True)
    status = models.SmallIntegerField(u'状态', default=UserStatus.WAIT_TO_AUDIT, choices=USER_STATUS_CHOICE)
    score = models.IntegerField(u'积分', default=0,)

    # likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="users_i_like", verbose_name=u'赞',
    #                                blank=True, null=True, through="UserLike")


    @models.permalink
    def get_absolute_url(self):
        return 'user_detail', [str(self.id)]

    def get_tags_from_cache(self):
        return CacheUtil.get_user_tags(self)

    def add_score(self, score):
        self.score = self.score + score
        self.save()

    def minus_score(self, score):
        if self.score > score:
            self.score = self.score - score
            self.save()

    def follow(self, followee):
        if self == followee:
            raise BusinessException(u'你不可以自己关注自己！')
        try:
            relationship = Relationship(from_person=self, to_person=followee)
            relationship.save()
        except IntegrityError:
            raise BusinessException(u'你已经关注了对方！')

    def is_default_avatar(self):
        return self.avatar in (settings.DEFAULT_MALE_AVATAR, settings.DEFAULT_FEMALE_AVATAR)

    def is_fake_user(self):
        return self.username.endswith('@1.com')

    def update_location(self, lat, lng, update_fake_user=False):
        if not update_fake_user and self.is_fake_user():
            return

        if self.location:
            user_location = self.location
        else:
            user_location = UserLocation()
        user_location.lat = lat
        user_location.lng = lng
        user_location.updated_at = datetime.now()
        user_location.save()
        if not self.location:
            self.location = user_location
            self.save()

    def audit_by_machine(self):
        if not self.avatar or self.is_default_avatar():
            if self.status not in (UserStatus.UNAPPROVED_BY_MACHINE, UserStatus.BLACKLIST, UserStatus.DELETED):
                self.status = UserStatus.UNAPPROVED_BY_MACHINE
                self.save()
        elif self.status not in (UserStatus.WAIT_TO_AUDIT, UserStatus.BLACKLIST, UserStatus.DELETED):
            self.status = UserStatus.WAIT_TO_AUDIT
            self.save()

    def is_following(self, another):
        if another.followers.filter(pk=self.pk):
            return True
        else:
            return False

    def get_payed_orders(self):
        return self.orders.filter(status__in=(OrderStatus.PAYIED, OrderStatus.USED)).order_by(
            "meal__start_date", "meal__start_time").cache()

    def get_passed_orders(self, my_payed_orders=None):
        if not my_payed_orders:
            my_payed_orders = self.get_payed_orders()
        my_passed_orders = []
        for order in my_payed_orders:
            if datetime.combine(order.meal.start_date, order.meal.start_time) <= datetime.now():
                my_passed_orders.append(order)
            # my_passed_orders.reverse()
        return my_passed_orders

    def get_upcomming_orders(self, my_payed_orders=None):
        if not my_payed_orders:
            my_payed_orders = self.get_payed_orders()
        my_upcomming_orders = []
        for order in my_payed_orders:
            if datetime.combine(order.meal.start_date, order.meal.start_time) > datetime.now():
                my_upcomming_orders.append(order)
        return my_upcomming_orders

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

    @property
    def age(self):
        if self.birthday:
            return date.today().year - self.birthday.year
        else:
            return None

    def avatar_thumbnail_for_size(self, avatar_size):
        return get_thumbnailer(self.avatar).get_thumbnail({
            'size': avatar_size,
            'box': self.cropping,
            'crop': True,
        }).url

    def avatar_thumbnail(self, width, height):
        return self.avatar_thumbnail_for_size((width, height))

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
    def followers(self):
        return self.followers.all()

    # @property
    # def upcoming_meals(self):
    #     return Meal.objects.filter(Q(host=self) | Q(participants=self)).filter(
    #         Q(start_date__gt=date.today()) |
    #         Q(start_date=date.today(), start_time__gt=datetime.now().time())).order_by(
    #         "start_date", "start_time")

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
        return [user for user in self.tags.similar_objects() if user.status == UserStatus.APPROVED]

    # return a list of values with the order how keys are sorted for a given dict
    def sortedDictValues(self, some_dict):
        from operator import itemgetter

        sortedItems = sorted(some_dict.items(), key=itemgetter(1))
        return [key[0] for key in sortedItems]

    @property
    def non_restaurant_usres(self):
        return User.objects.exclude(restaurant__isnull=False)

    def users_nearby(self, lat=None, lng=None):
        distance_user_dict = {}
        if lat and lng:
            lat = float(lat)
            lng = float(lng)
        elif self.location:
            lat = self.location.lat
            lng = self.location.lng
        if not lat or not lng:
            return []
            # for user in self.non_restaurant_usres.exclude(pk=self.id): #.exclude(pk__in=self.following.values('id')):
        for user in User.objects.filter(status=UserStatus.APPROVED).exclude(pk=self.id):
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
            location.lat = settings.FAKED_LAT
            location.lng = settings.FAKED_LNG
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
        return \
            self.messages.filter(type=0).filter(Q(from_person=other_user) | Q(to_person=other_user)).order_by(
                'timestamp')[
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

    def get_total_unread_message_count(self):
        return get_unread_message_count(self.username)

    def get_total_unread_noty_count(self):
        return get_unread_noty_count(self.username)

    def get_webio_client(self):
        weibo_client = weibo.APIClient(app_key=settings.WEIBO_APP_KEY, app_secret=settings.WEIBO_APP_SECERT,
                                       redirect_uri=settings.WEIBO_REDIRECT_URL)
        weibo_client.set_access_token(self.weibo_access_token, str(3600 * 24 * 14))
        return weibo_client

    def __unicode__(self):
        return self.name if self.name is not None else self.username

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = u'用户'


class ClientSource:
    IOS = 0
    WEB = 1


class UserSource(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=u'用户',)
    source = models.IntegerField(u'注册来源', default=ClientSource.IOS)


class UserPhoto(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="photos")
    photo = models.ImageField(upload_to='uploaded_images/%Y/%m/%d', max_length=256)
    timestamp = models.DateTimeField(u'时间', blank=True, auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="photos_i_like", verbose_name=u'赞',
                                   blank=True, null=True, through="PhotoLike")

    def __unicode__(self):
        return str(self.id)

    @property
    def photo_thumbnail(self):
        try:
            return get_thumbnailer(self.photo).get_thumbnail({'size': (210, 210),
                                                              'crop': True,
            }).url
        except Exception:
            return None

    @property
    def large_photo(self):
        try:
            return get_thumbnailer(self.photo).get_thumbnail({'size': (710, 1400 ),
                                                              'crop': False,
            }).url
        except Exception:
            return None

    @property
    def likes_count(self):
        return PhotoLike.objects.filter(target=self).count()

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

MEAL_PERSON_CHOICE = [(2 * x, "%s 人" % (2 * x)) for x in range(1, 5)]
START_TIME_CHOICE = ((dtime(6, 00), "6:00"), (dtime(7, 00), "7:00"), (dtime(8, 00), "8:00"),
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
    list_price = models.DecimalField(u'均价', max_digits=6, decimal_places=1, default=30.0,
                                     blank=True, null=True)
    extra_requests = models.CharField(u'其它要求', max_length=128, null=True, blank=True)
    status = models.SmallIntegerField(u'饭局状态', choices=MEAL_STATUS_CHOICE, default=MealStatus.CREATED_NO_MENU)
    max_persons = models.IntegerField(u'最多参加人数', default=0, blank=True, null=True) # not used for now,
    photo = models.ImageField(u'饭局封面', null=True, blank=True,
                              upload_to='uploaded_images/%Y/%m/%d') #if none use menu's cover
    cropping = ImageRatioField('photo', '420x280')
    restaurant = models.ForeignKey(Restaurant, verbose_name=u'餐厅', blank=True, null=True) #TODO retrieve from menu
    menu = models.ForeignKey(Menu, verbose_name=u'菜单', null=True, blank=True)
    host = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="host_user",
                             verbose_name=u'发起者', )
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="meals", verbose_name=u'参加者',
                                          blank=True, null=True,
                                          through="MealParticipants")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="meals_i_like", verbose_name=u'喜欢该饭局的人',
                                   blank=True, null=True, through="MealLike")
    actual_persons = models.IntegerField(u'实际参加人数', default=0)
    type = models.IntegerField(default=0) # THEMES, DATES


    @classmethod
    def get_all_meals(cls):
        return Meal.objects.filter(status=MealStatus.PUBLISHED, privacy=MealPrivacy.PUBLIC).order_by('start_date',
                                                                                                     'start_time')


    @classmethod
    def get_upcomming_meals(cls, all_meals=None):
        if not all_meals:
            all_meals = cls.get_all_meals()
        upcomming_meals = []
        for meal in all_meals:
            if datetime.combine(meal.start_date, meal.start_time) >= datetime.now() - timedelta(hours=3):
                upcomming_meals.append(meal)
        return upcomming_meals


    @classmethod
    def get_passed_meals(cls, all_meals=None):
        if not all_meals:
            all_meals = cls.get_all_meals()
        passed_meals = []
        for meal in all_meals:
            if datetime.combine(meal.start_date, meal.start_time) < datetime.now() - timedelta(hours=3):
                passed_meals.append(meal)
        passed_meals.reverse()
        return passed_meals

    @property
    def likes_count(self):
        return MealLike.objects.filter(target=self).count()

    def checkAvaliableSeats(self, customer, requesting_persons):
        other_paying_orders = self.orders.exclude(customer=customer).exclude(
            customer__in=self.participants.all()).filter(status=OrderStatus.CREATED,
                                                         created_time__gte=datetime.now() - timedelta(
                                                             minutes=settings.PAY_OVERTIME)).select_for_update().values(
            'customer').annotate(max_num_persons=Max('num_persons'))
        paying_persons = sum([o['max_num_persons'] for o in other_paying_orders])
        if self.actual_persons + requesting_persons + paying_persons > self.max_persons:
            if self.actual_persons >= self.max_persons:
                message = u'已经爆满了！'
            elif paying_persons == 0:
                message = u'最多只可以预定%s个座位！' % (self.max_persons - self.actual_persons)
            elif requesting_persons > self.max_persons - self.actual_persons - paying_persons > 0:
                message = u'现在有%s位用户正在支付，最多只可以预定%s个座位，你可以%s分钟后再尝试预定！' % (
                    paying_persons, self.max_persons - self.actual_persons - paying_persons,
                    settings.PAY_OVERTIME_FOR_PAY_OR_USER)
            else:
                message = u'现在有%s位用户正在支付，你可以%s分钟后再尝试预定！' % (paying_persons, settings.PAY_OVERTIME_FOR_PAY_OR_USER)
            raise NoAvailableSeatsError(message)

    def join(self, customer, requesting_persons):
        if self.is_participant(customer):
            raise AlreadyJoinedError(u"对不起，您已经报名了！")

        self.checkAvaliableSeats(customer, requesting_persons)

        order = Order()
        order.meal = self
        order.customer = customer
        order.num_persons = requesting_persons
        order.orginal_total_price = self.list_price * requesting_persons
        # if customer.is_staff:
        #     order.total_price = 0.1 * requesting_persons
        # else:
        order.total_price = order.orginal_total_price
        order.status = OrderStatus.CREATED
        order.save()
        return order

    @property
    def is_passed(self):
        return self.start_date < date.today() or (
            self.start_date == date.today() and self.start_time < datetime.now().time())

    @property
    def paid_orders(self):
        return Order.objects.filter(meal=self, status__in=(OrderStatus.PAYIED, OrderStatus.USED)).select_related(
            'customer')

    def is_participant(self, user):
        return self.participants.filter(pk=user.id).exists()

    @property
    def comments(self):
        return self.comments.all()

    @property
    def left_persons(self):
        return self.max_persons - self.actual_persons

    def get_cover_thumbnail(self, size):
        return get_thumbnailer(self.photo).get_thumbnail({
            'size': size,
            'crop': True,
            'box': self.cropping
        }).url

    @property
    def big_cover_url(self):
        if self.photo:
            url = self.get_cover_thumbnail(settings.BIG_MENU_COVER_SIZE)
        else:
            url = self.menu.big_cover_url
        return url

    @property
    def normal_cover_path(self):
        if self.photo:
            path = get_thumbnailer(self.photo).get_thumbnail({
                'size': settings.NORMAL_MENU_COVER_SIZE,
                'crop': True,
                'box': self.cropping
            }).path
        else:
            path = self.menu.normal_cover_path
        return path

    @property
    def normal_cover_url(self):
        if self.photo:
            url = self.get_cover_thumbnail(settings.NORMAL_MENU_COVER_SIZE)
        else:
            url = self.menu.normal_cover_url
        return url


    @property
    def small_cover_url(self):
        if self.photo:
            url = self.get_cover_thumbnail(settings.SMALL_MENU_COVER_SIZE)
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

# Like.enable_like(Meal)

# class MealLike(models.Model):
#     meal = models.ForeignKey(Meal)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL)
#
#     def __unicode__(self):
#         return u"%s参加了饭局%s" % (self.user, self.meal)
#
#     class Meta:
#         ordering = ['id', ]
#         verbose_name = u'饭局参加者'
#         verbose_name_plural = verbose_name

# class Like(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'Owner', related_name='likes')
#
#     content_type = models.ForeignKey(ContentType)
#     object_id = models.PositiveIntegerField()
#     target = generic.GenericForeignKey('content_type', 'object_id')
#
#     @classmethod
#     def add_like(self, content_type, object_id, user):
#         like, created = Like.objects.get_or_create(user=user, content_type=content_type, object_id=object_id)
#         return created
#
#     @classmethod
#     def enable_like(self, cls):
#
#         def likes(self):
#             content_type = ContentType.objects.get_for_model(self)
#             return Like.objects.filter(content_type=content_type, object_id=self.id).select_related("user")
#
#         def likes_count(self):
#             content_type = ContentType.objects.get_for_model(self)
#             return Like.objects.filter(content_type=content_type, object_id=self.id).count()
#
#         def add_like(self, user):
#             content_type = ContentType.objects.get_for_model(self)
#             like, created = Like.objects.get_or_create(user=user, content_type=content_type, object_id=self.id)
#             return created
#
#         cls.add_to_class("likes_count", property(likes_count))
#         cls.add_to_class("likes", property(likes))
#         cls.add_to_class("add_like", add_like)
#
#     class Meta:
#         unique_together = (('user', 'content_type', 'object_id'),)



# class Like(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'用户', blank=True)
#
#     @classmethod
#     def get_like_class(cls, like_type):
#         like_content_type = u"%slike" % comment_type
#         content_type = ContentType.objects.get_by_natural_key("fanju", like_content_type)
#         model_cls = content_type.model_class()
#         return model_cls
#
#     @classmethod
#     def get_likes(cls, like_type, target_id):
#         return cls.get_like_class(like_type).objects.filter(target_id=target_id).select_related('user')
#
#     @classmethod
#     def get_likes_count(cls, like_type, target_id):
#         return cls.get_like_class(like_type).objects.filter(target_id=target_id).count()
#
#     @classmethod
#     def add_like(self, user):
#             content_type = ContentType.objects.get_for_model(self)
#             like, created = Like.objects.get_or_create(user=user, content_type=content_type, object_id=self.id)
#             return created
#
#     @classmethod
#     def enable_like(self, cls):
#
#         # def likes(self):
#         #     content_type = ContentType.objects.get_for_model(self)
#         #     return Like.objects.filter(content_type=content_type, object_id=self.id).select_related("user")
#
#         def likes_count(self):
#             like_type = 'meal' #TODO
#             content_type = ContentType.objects.get_for_model(self)
#             return Like.get_likes_count(like_type, self.id)
#
#         def add_like(self, user):
#             content_type = ContentType.objects.get_for_model(self)
#             like, created = Like.objects.get_or_create(user=user, content_type=content_type, object_id=self.id)
#             return created
#
#         cls.add_to_class("likes_count", property(likes_count))
#         cls.add_to_class("likes", property(likes))
#         cls.add_to_class("add_like", add_like)
#
#     def __unicode__(self):
#         return '[%s] %s' % (self.id, self.comment[:20])
#
#
#     class Meta:
#         abstract = True


class MealParticipants(models.Model):
    meal = models.ForeignKey(Meal)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return u"%s参加了饭局%s" % (self.user, self.meal)

    class Meta:
        ordering = ['id', ]
        verbose_name = u'饭局参加者'
        verbose_name_plural = verbose_name


class ObjectType:
    MEAL = 'meal'
    USER = 'user'
    PHOTO = 'photo'
    GROUP = 'group'


class CommentStatus(AuditStatus):
    pass


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'作者', blank=True)
    comment = models.CharField(u'评论', max_length=200)
    timestamp = models.DateTimeField(u'时间', blank=True, auto_now_add=True)
    status = models.SmallIntegerField(u'状态', default=CommentStatus.WAIT_TO_AUDIT, choices=AUDIT_STATUS_CHOICE)
    parent = models.ForeignKey('self', verbose_name=u'父评论', blank=True, null=True)

    @classmethod
    def get_comment_class(cls, comment_type):
        comment_content_type = u"%scomment" % comment_type
        content_type = ContentType.objects.get_by_natural_key("fanju", comment_content_type)
        model_cls = content_type.model_class()
        return model_cls

    @classmethod
    def get_comments(cls, comment_type, target_id):
        return cls.get_comment_class(comment_type).objects.filter(target_id=target_id, status__in=(
            CommentStatus.WAIT_TO_AUDIT, CommentStatus.APPROVED)).select_related('parent__user', 'user')

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
            result = u'刚刚'
        return result

    def __unicode__(self):
        return '[%s] %s' % (self.id, self.comment[:20])


    class Meta:
        abstract = True


class MealComment(Comment):
    target = models.ForeignKey(Meal, verbose_name=u'被评论的饭局', related_name='comments')

    def get_absolute_url(self):
        return '%s#comment-%d' % (reverse_lazy('meal_detail', kwargs={'meal_id': self.target_id}), self.id)

    class Meta:
        verbose_name = u'评论饭局'
        verbose_name_plural = verbose_name


class PhotoComment(Comment):
    target = models.ForeignKey(UserPhoto, verbose_name=u'被评论的照片', related_name='comments')

    def get_absolute_url(self):
        return '%s#comment-%d' % (reverse_lazy('photo_detail', kwargs={'pk': self.target_id}), self.id)

    class Meta:
        verbose_name = u'评论照片'
        verbose_name_plural = verbose_name


class UserComment(Comment):
    target = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'被评论的用户', related_name='comments')

    class Meta:
        verbose_name = u'评论用户'
        verbose_name_plural = verbose_name


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True


class MealLike(Like):
    target = models.ForeignKey(Meal, verbose_name=u'饭局')

    class Meta:
        verbose_name = u'赞饭局'
        verbose_name_plural = verbose_name


class PhotoLike(Like):
    target = models.ForeignKey(UserPhoto, verbose_name=u'照片')

    class Meta:
        verbose_name = u'赞照片'
        verbose_name_plural = verbose_name
#
#
# class UserLike(Like):
#     target = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'用户')
#
#     class Meta:
#         verbose_name = u'赞用户'
#         verbose_name_plural = verbose_name

# class ImageTest(models.Model):
#     image = ImageField(blank=True, null=True, upload_to='apps')
#     # size is "width x height"
#     cropping = ImageRatioField('image', '640x640')

####################################################  POST SAVE   #######################################

@receiver(post_save, sender=User, dispatch_uid='profile_changed')
def profile_changed(sender, instance, created, **kwargs):
    set_default_avatar(instance)
    cache.set(CacheKey.USER_TAG % instance.id, None)


def set_default_avatar(user):
    need_set_default_avatar = False
    if not user.avatar:
        need_set_default_avatar = True
    elif user.gender == Gender.FEMALE and user.avatar == settings.DEFAULT_MALE_AVATAR:
        need_set_default_avatar = True
    elif user.gender != Gender.FEMALE and user.avatar == settings.DEFAULT_FEMALE_AVATAR:
        need_set_default_avatar = True

    if need_set_default_avatar:
        if user.gender == Gender.FEMALE:
            user.avatar = settings.DEFAULT_FEMALE_AVATAR
        else:
            user.avatar = settings.DEFAULT_MALE_AVATAR
        user.cropping = ''
        user.save(update_fields=('avatar', 'cropping'))

# @receiver(post_save, sender=User, dispatch_uid='set_default_audit')
# def set_default_audit(sender, instance, created, **kwargs):
#     user = instance
#     if not user.avatar or user.is_default_avatar() or user.tags.count() < 3:
#         if user.status in (AuditStatus.UNFLAGGED, AuditStatus.APPROVED):
#             user.status = AuditStatus.UNAPPROVED_BY_MACHINE
#             user.save(update_fields=('status', ))
#
#     elif user.status not in (AuditStatus.UNFLAGGED,):
#         user.status = AuditStatus.UNFLAGGED
#         user.save(update_fields=('status', ))


#my followee do sth
node_followee_join_meal = "/user/%d/meals"
node_followee_upload_photo = "/user/%d/photos"

#sb do sth to me or my staff
node_photo_comment = "/user/%d/photos/comments"
node_comment_reply = "/user/%d/comments/reply"
node_visitor = "/user/%d/visitors"
node_follower = "/user/%d/followers"
node_photo_request = "/user/%d/photo_requests"

#sb do sth to meal which I joined
node_meal_comment = "/meal/%d/comments"
node_meal_participant = "/meal/%d/participants"


def _pubsub_user_created(user):
    cl_create_node, _ = pubsub.create_client()
    pubsub.create_node(node_followee_join_meal % user.id, client=cl_create_node)
    pubsub.create_node(node_followee_upload_photo % user.id, client=cl_create_node)
    pubsub.create_node(node_photo_comment % user.id, client=cl_create_node)
    pubsub.create_node(node_comment_reply % user.id, client=cl_create_node)
    pubsub.create_node(node_visitor % user.id, client=cl_create_node)
    pubsub.create_node(node_follower % user.id, client=cl_create_node)
    pubsub.create_node(node_photo_request % user.id, client=cl_create_node)
    cl_create_node.disconnect()

    cl_user, _ = pubsub.create_client(user=user)
    pubsub.subscribe(user, node_photo_comment % user.id, client=cl_user)
    pubsub.subscribe(user, node_comment_reply % user.id, client=cl_user)
    pubsub.subscribe(user, node_visitor % user.id, client=cl_user)
    pubsub.subscribe(user, node_follower % user.id, client=cl_user)
    pubsub.subscribe(user, node_photo_request % user.id, client=cl_user)
    cl_user.disconnect()


@receiver(post_save, sender=User, dispatch_uid="pubsub_user_created")
def pubsub_user_created(sender, instance, created, **kwargs):
    if created:
        # _pubsub_user_created(instance)
        t = threading.Thread(target=_pubsub_user_created, args=(instance,))
        t.start()


@receiver(post_save, sender=Relationship, dispatch_uid="user_followed")
def user_followed(sender, instance, created, **kwargs):
    if created:
        followee = instance.to_person
        follower = instance.from_person
        event = u'关注了你'

        payload = json.dumps({"user": follower.id,
                              "avatar": follower.normal_avatar,
                              "s_avatar": follower.small_avatar,
                              "name": follower.name,
                              "message": u"%s%s" % (follower.name, event),
                              "event": event})

        pubsub.publish(node_follower % followee.id, payload)

        cl, _ = pubsub.create_client(follower)
        pubsub.subscribe(follower, node_followee_join_meal % followee.id, client=cl)
        pubsub.subscribe(follower, node_followee_upload_photo % followee.id, client=cl)
        cl.disconnect()


@receiver(post_delete, sender=Relationship, dispatch_uid="user_unfollowed")
def user_unfollowed(sender, instance, **kwargs):
    followee = instance.to_person
    follower = instance.from_person
    cl, _ = pubsub.create_client(follower)
    pubsub.unsubscribe(follower, node_followee_join_meal % followee.id, client=cl)
    pubsub.unsubscribe(follower, node_followee_upload_photo % followee.id, client=cl)
    cl.disconnect()


@receiver(post_save, sender=Meal, dispatch_uid="meal_created")
def meal_created(sender, instance, created, **kwargs):
    if created:
        meal = instance
        host = meal.host
        node_name = node_meal_participant % meal.id
        pubsub.create_node(node_name)
        pubsub.subscribe(host, node_name)

        node_name = node_meal_comment % meal.id
        pubsub.create_node(node_name)
        pubsub.subscribe(host, node_name)


def _meal_joined(meal, joiner, participant=None):
    if meal.host and meal.host.id == joiner.id:
        event = u"发起了活动"
    else:
        event = u"参加了活动"
    payload = json.dumps({
        "user": joiner.id,
        "avatar": joiner.normal_avatar,
        "s_avatar": joiner.small_avatar,
        "name": joiner.name,
        "message": u"%s%s：%s" % (joiner.name, event, meal.topic),
        "event": event,
        "meal": meal.id,
        "topic": meal.topic,
        "meal_photo": meal.small_cover_url,
        "meal_participant": participant.id})
    if not meal.host or meal.host.id != joiner.id:
        # host does not publish meal events to participants
        # and he has subscribed the events already when he created the meal
        pubsub.publish(node_meal_participant % meal.id, payload)
        pubsub.subscribe(joiner, node_meal_participant % meal.id)

        pubsub.subscribe(joiner, node_meal_comment % meal.id)

        #TODO how about quit the meal
    #remove the subscription for of the user who is the joiner of the meal
    # and is also the  follower of the joiner, to prevent duplicate notification'
    users_to_unsubscribe = meal.participants.filter(id__in=joiner.followers.all())
    followee_join_meal_node = node_followee_join_meal % joiner.id
    for user in users_to_unsubscribe:
        pubsub.unsubscribe(user, followee_join_meal_node)
        #    time.sleep(1)
    pubsub.publish(followee_join_meal_node, payload)
    for user in users_to_unsubscribe:
        pubsub.subscribe(user, followee_join_meal_node)


@receiver(post_save, sender=MealParticipants, dispatch_uid="meal_joined")
def meal_joined(sender, instance, created, **kwargs):
    if created:
        t = threading.Thread(target=_meal_joined, args=(instance.meal, instance.user, instance))
        t.start()


@receiver(post_save, sender=Visitor, dispatch_uid="user_visited")
def user_visited(sender, instance, created, **kwargs):
    if created:
        visitor = instance.from_person
        if visitor.id != instance.to_person.id:
            node_name = node_visitor % instance.to_person.id
            event = u"查看了你的个人资料"
            payload = json.dumps({"user": visitor.id,
                                  "avatar": visitor.normal_avatar,
                                  "s_avatar": visitor.small_avatar,
                                  "name": visitor.name,
                                  "message": u"%s%s" % (visitor.name, event),
                                  "event": event,
            })
            pubsub.publish(node_name, payload)


@receiver(post_save, sender=PhotoRequest, dispatch_uid="photo_request")
def photo_requested(sender, instance, created, **kwargs):
    if created:
        requestor = instance.from_person
        if requestor.id != instance.to_person.id:
            node_name = node_photo_request % instance.to_person.id
            event = u"邀请你上传照片"
            payload = json.dumps({"user": requestor.id,
                                  "avatar": requestor.normal_avatar,
                                  "s_avatar": requestor.small_avatar,
                                  "name": requestor.name,
                                  "message": u"%s%s" % (requestor.name, event),
                                  "event": event,
            })
            pubsub.publish(node_name, payload)


@receiver(post_save, sender=UserPhoto, dispatch_uid="photo_uploaded")
def photo_uploaded(sender, instance, created, **kwargs):
    if created:
        node_name = node_followee_upload_photo % instance.user.id
        event = u"上传了一张照片"
        payload = json.dumps({"user": instance.user.id,
                              "avatar": instance.user.normal_avatar,
                              "s_avatar": instance.user.small_avatar,
                              "name": instance.user.name,
                              "message": u"%s%s" % (instance.user.name, event),
                              "event": event,
                              "photo_id": instance.id,
                              "photo_url": instance.photo.url,
                              "photo": instance.photo_thumbnail})
        pubsub.publish(node_name, payload)
        instance.user.add_score(Score.UPLOAD_PHOTO)


@receiver(post_save, sender=PhotoComment, dispatch_uid="photo_comment")
def photo_commented(sender, instance, created, **kwargs):
    comment = instance

    if created:
        photo_owner = comment.target.user
        comment_author = comment.user
        reply_to = comment.parent.user if comment.parent_id else None
        print "%s %s %s" % ( photo_owner, comment_author, reply_to)
        if reply_to and comment_author != reply_to:
            event = u'回复了你'
            comment_content = comment.comment[:12] + ("..." if len(comment.comment) > 12 else  "")
            payload = json.dumps({"user": comment.user.id,
                                  "avatar": comment.user.normal_avatar,
                                  "s_avatar": comment.user.small_avatar,
                                  "name": comment.user.name,
                                  "message": u"%s%s" % (comment.user.name, event),
                                  "event": event,
                                  "photo_id": comment.target.id,
                                  "comment_id": comment.id,
                                  "comment": u'“%s”' % comment_content})
            pubsub.publish(node_comment_reply % reply_to.id, payload)

        if comment_author != photo_owner and (reply_to is None or reply_to != photo_owner):
            event = u'评论了你的照片'
            comment_content = comment.comment[:12] + ("..." if len(comment.comment) > 12 else  "")
            payload = json.dumps({"user": comment.user.id,
                                  "avatar": comment.user.normal_avatar,
                                  "s_avatar": comment.user.small_avatar,
                                  "name": comment.user.name,
                                  "message": u"%s%s" % (comment.user.name, event),
                                  "event": event,
                                  "photo_id": comment.target.id,
                                  "comment_id": comment.id,
                                  "comment": u'“%s”' % comment_content})
            pubsub.publish(node_photo_comment % photo_owner.id, payload)


@receiver(post_save, sender=MealComment, dispatch_uid="meal_comment")
def meal_commented(sender, instance, created, **kwargs):
# 被回复的人和我自己先 unsubscribe meal comment
# 通知饭局参加者
# 再通知被回复的人
# 被回复的人和我自己再subscribe meal comment
    comment = instance
    if created:
        comment_author = comment.user
        reply_to = comment.parent.user if comment.parent_id else None
        meal = comment.target
        meal_participants = meal.participants.all()
        user_to_unsubscribe_meal_comment = [user for user in (comment_author, reply_to) if
                                            user and user in meal_participants]
        for user in user_to_unsubscribe_meal_comment:
            pubsub.unsubscribe(user, node_meal_comment % meal.id, )

        comment_content = comment.comment[:12] + ("..." if len(comment.comment) > 12 else  "")
        playlaod_json = {"user": comment.user.id,
                         "avatar": comment.user.normal_avatar,
                         "s_avatar": comment.user.small_avatar,
                         "name": comment.user.name,
                         "meal_id": comment.target.id,
                         "comment_id": comment.id,
                         "comment": u'“%s”' % comment_content}

        if len(meal_participants):
            event = u"评论了活动 “%s”" % meal.topic[:9]
            playlaod_json['event'] = event
            playlaod_json['message'] = u"%s%s" % (comment.user.name, event)
            pubsub.publish(node_meal_comment % meal.id, json.dumps(playlaod_json))

        for user in user_to_unsubscribe_meal_comment:
            pubsub.subscribe(user, node_meal_comment % meal.id, )

        if reply_to and comment_author != reply_to:
            event = u'回复了你'
            playlaod_json['event'] = event
            playlaod_json['message'] = u"%s%s" % (comment.user.name, event)
            pubsub.publish(node_comment_reply % reply_to.id, json.dumps(playlaod_json))

#
# @receiver(post_save, sender=Order, dispatch_uid="order_changed")
# def order_changed(sender, instance, created, **kwargs):
#     order = instance
#
#     if not order.status == OrderStatus.CREATED:
#         cache.set(CacheKey.MEAL_PAYED_ORDERS % order.meal.id, None)
