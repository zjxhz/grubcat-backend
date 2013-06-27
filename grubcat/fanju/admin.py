#coding=utf-8
from ajax_select.admin import AjaxSelectAdmin
from django import forms
from django.contrib import admin
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.admin import UserAdmin
from django.forms.extras import SelectDateWidget
from taggit.utils import edit_string_for_tags
from fanju.forms import BasicProfileForm
from fanju.models import Restaurant, Dish, DishCategory, Order, Meal, Menu, \
    UserTag, DishItem, DishCategoryItem, TransFlow, MealComment, PhotoComment, \
    UserComment, photo_requested, User, meal_joined, MealParticipants, user_followed, \
    Relationship, user_visited, Visitor, photo_uploaded, UserPhoto, \
    pubsub_user_created, PhotoRequest, meal_created, AuditStatus
from image_cropping.admin import ImageCroppingMixin
import datetime


def approve(self, request, queryset):
    queryset.update(status=AuditStatus.APPROVED)
    self.message_user(request, "审核通过!")


approve.short_description = u"审核通过"


def un_approve(self, request, queryset):
    queryset.update(status=AuditStatus.UNAPPROVED_BY_ADMIN)
    self.message_user(request, "审核不通过!")


un_approve.short_description = u"审核不通过"


def make_delete(self, request, queryset):
    queryset.update(status=AuditStatus.DELETED)
    self.message_user(request, "成功标记为删除状态!")


make_delete.short_description = u"标记为删除状态"

audit_actions = [approve, un_approve, make_delete]


class UserCreationForm(auth_forms.UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    class Meta:
        model = User
        fields = (
            'username', 'password', 'name', 'weibo_id', 'gender', 'avatar', 'cropping', 'tags', 'constellation',
            'birthday', 'college', 'industry', 'work_for', 'occupation', 'motto', 'weibo_access_token', 'is_staff',
            'is_superuser',
            'apns_token')
        widgets = {
            'birthday': SelectDateWidget(required=False, years=range(1976, 1996), attrs={'class': "input-small"}, )

        }


class UserChangeForm(auth_forms.UserChangeForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    class Meta:
        model = User
        fields = (
            'username', 'password', 'name', 'weibo_id', 'gender', 'avatar', 'cropping', 'tags', 'constellation',
            'birthday', 'college', 'industry', 'work_for', 'occupation', 'motto', 'weibo_access_token', 'is_staff',
            'is_superuser', 'status',
            'apns_token')
        widgets = {
            'birthday': SelectDateWidget(required=False, years=range(1976, 1996), attrs={'class': "input-small"}, )

        }


class UserAdmin(ImageCroppingMixin, UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    def avatar_thumb(self, instance):
        # if instance.is_default_avatar():
        #     return '无头像'
        # else:
        return '<img src="%s"/>' % (instance.small_avatar)
    avatar_thumb.allow_tags = True
    avatar_thumb.short_description = u'头像'

    def tags_plain(self, instance):
        return edit_string_for_tags(instance.tags.all())
    tags_plain.short_description = u'兴趣'

    list_display = ('id', 'username', 'name', 'weibo_id', 'avatar_thumb', 'tags_plain', 'motto', 'status', )
    list_filter = ('status', 'is_staff', 'is_superuser', 'is_active', 'groups')
    list_editable = ('status', )
    fieldsets = (
        (None, {'fields': ('username', 'password', 'name', 'weibo_id', 'gender', 'avatar', 'cropping', 'tags', 'status')}),
        ('Others', {'fields': (
            'constellation', 'birthday', 'college', 'industry', 'work_for', 'occupation', 'motto', 'weibo_access_token',
            'apns_token', 'is_staff', 'is_superuser',)}),
    )
    add_fieldsets = (
        (None, {
            'fields': (
                'username', 'password1', 'password2', 'name', 'weibo_id', 'gender', 'avatar', 'cropping', 'tags')}),
        ('Others', {'fields': (
            'constellation', 'birthday', 'college', 'industry', 'work_for', 'occupation', 'motto', 'weibo_access_token',
            'apns_token', 'is_staff', 'is_superuser',)})
    )
    search_fields = ('username',)
    ordering = ('-id',)

    actions = ['resend_message'] + audit_actions

    def resend_message(self, request, queryset):
        for user in queryset:
            pubsub_user_created(User, user, True)
        self.message_user(request, "成功发送用户创建消息!")

    resend_message.short_description = u"重新发送用户创建消息"


class DishAdmin(AjaxSelectAdmin):
#    form = make_ajax_form(Dish,{'categories':'dish_category'})
    list_display = ('restaurant', 'name', 'price', 'unit', 'available',)
    list_editable = ('name', 'price', 'unit', 'available', )
    list_display_links = ('restaurant',)
    list_filter = ('restaurant',)
    ordering = ('restaurant',)


class DishCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'restaurant')


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'meal', 'customer', 'created_time', 'payed_time', 'completed_time', 'status', 'num_persons', 'code',
        'total_price', 'orginal_total_price', 'flow')
    list_filter = ('meal', 'status')
    ordering = ('-id', 'meal', 'status',)
    actions = ['cancel_order']

    def cancel_order(self, request, queryset):
        for order in queryset:
            order.cancel()
        self.message_user(request, "订单取消成功!")

    cancel_order.short_description = u"取消订单"


class TransFlowAdmin(admin.ModelAdmin):
    list_display = ('order', 'alipay_trade_no')


class MealAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('id', 'topic', 'restaurant', 'menu', 'host', 'list_price', 'actual_persons')
    list_filter = ('start_date', 'restaurant')
    ordering = ('menu', )
    actions = ['resend_message', 'postpone_meal']

    def resend_message(self, request, queryset):
        for meal in queryset:
            meal_created(MealAdmin, meal, True)
        self.message_user(request, "成功发饭局创建消息!")

    resend_message.short_description = u"重新发送饭局创建消息"

    def postpone_meal(self, request, queryset):
        for meal in queryset:
            meal.start_date += datetime.timedelta(days=31)
            meal.save()
        self.message_user(request, "延期成功!")

    postpone_meal.short_description = u"延期1个月"


class DishItemInline(admin.StackedInline):
    model = DishItem


class DishCategoryItemInline(admin.StackedInline):
    model = DishCategoryItem


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'latitude', 'longitude', 'address')


class MenuAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'restaurant', 'status', 'num_persons', 'average_price',)
    list_filter = ('restaurant', 'status')
    inlines = [DishItemInline, DishCategoryItemInline]
    ordering = ('status',)


class MealParticipantsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'meal')
    actions = ['resend_message']

    def resend_message(self, request, queryset):
        for participant in queryset:
            meal_joined(MealParticipants, participant, True)
        self.message_user(request, "成功发送加入饭局消息!")

    resend_message.short_description = u"重新发送加入饭局消息"


class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_person', 'to_person')
    actions = ['resend_message']

    def resend_message(self, request, queryset):
        for relationship in queryset:
            user_followed(Relationship, relationship, True)
        self.message_user(request, "成功发送用户关注消息!")

    resend_message.short_description = u"重新发送用户关注消息"


class VisitorAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_person', 'to_person')
    actions = ['resend_message']

    def resend_message(self, request, queryset):
        for visitor in queryset:
            user_visited(Visitor, visitor, True)
        self.message_user(request, "成功发送用户访问消息!")

    resend_message.short_description = u"重新发送用户访问消息"


class PhotoRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_person', 'to_person')
    actions = ['resend_message']

    def resend_message(self, request, queryset):
        for photo_request in queryset:
            photo_requested(PhotoRequest, photo_request, True)
        self.message_user(request, "成功发送求照片消息!")

    resend_message.short_description = u"重新发送求照片消息"


class UserPhotoAdmin(admin.ModelAdmin):

    def photo_thumb(self, instance):
        return '<img src="%s"/>' % (instance.photo_thumbnail)
    photo_thumb.allow_tags = True
    photo_thumb.short_description = u'照片'

    list_display = ('id', 'user', 'photo_thumb')
    actions = ['resend_message']

    def resend_message(self, request, queryset):
        for up in queryset:
            photo_uploaded(UserPhoto, up, True)
        self.message_user(request, "成功发送用户上传照片消息!")

    resend_message.short_description = u"重新发送用户上传照片消息"


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'target', 'user', 'comment', 'status',)
    list_filter = ('status', 'target',)
    list_editable = ('status',)
    ordering = ('-target', '-id')
    actions = audit_actions


admin.site.register(Meal, MealAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(TransFlow, TransFlowAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(DishCategory, DishCategoryAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(UserTag)
admin.site.register(MealComment, CommentAdmin)
admin.site.register(PhotoComment, CommentAdmin)
admin.site.register(UserComment, CommentAdmin)
admin.site.register(User, UserAdmin)
# admin.site.register(GroupCategory)
# admin.site.register(Group, GroupAdmin)
# admin.site.register(GroupComment, GroupCommentAdmin)
admin.site.register(MealParticipants, MealParticipantsAdmin)
admin.site.register(Relationship, RelationshipAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(PhotoRequest, PhotoRequestAdmin)
admin.site.register(UserPhoto, UserPhotoAdmin)

