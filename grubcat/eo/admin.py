#coding=utf-8
from ajax_select.admin import AjaxSelectAdmin
from django.contrib import admin
from eo.models import Restaurant, Dish, DishCategory, Order, Meal, Menu, UserTag, \
    DishItem, DishCategoryItem, GroupComment, TransFlow
from grubcat.eo.models import meal_joined, MealParticipants, user_followed, \
    Relationship, user_visited, Visitor, photo_uploaded, UserPhoto
from image_cropping.admin import ImageCroppingMixin
from models import Group, GroupCategory, UserProfile, ImageTest
import datetime

class UserProfileAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('id','name','weibo_id','avatar','cropping')
    list_editable = ('name','avatar',)
class DishAdmin(AjaxSelectAdmin):
#    form = make_ajax_form(Dish,{'categories':'dish_category'})
    list_display = ('restaurant', 'name', 'price', 'unit', 'available',)
    list_editable = ('name', 'price', 'unit', 'available', )
    list_display_links = ('restaurant',)
    list_filter = ('restaurant',)
    ordering = ('restaurant',)

class DishCategoryAdmin(admin.ModelAdmin):
    list_display =('name', 'restaurant')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','meal', 'customer', 'created_time','payed_time','completed_time','status', 'num_persons', 'code','total_price','flow')
    list_filter = ('meal', 'status')
    ordering = ('-id','meal', 'status',)
    actions = ['cancel_order']
    def cancel_order(self, request, queryset):
        for order in queryset:
            order.cancel()
        self.message_user(request, "订单取消成功!")
    cancel_order.short_description = u"取消订单"

class TransFlowAdmin(admin.ModelAdmin):
    list_display = ('order','alipay_trade_no')

class MealAdmin(admin.ModelAdmin):
    list_display = ('topic', 'menu','host', 'list_price','actual_persons')
    list_filter = ('start_date',)
    ordering = ('menu', )
    actions = ['postpone_meal']
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
    list_display = ('name','latitude','longitude','address')

class MenuAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('restaurant','status','id','num_persons','average_price',)
    list_filter = ('restaurant','status')
    inlines = [DishItemInline,DishCategoryItemInline]
    ordering = ('status',)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('id','name','category')
    list_filter = ('category',)
    list_editable = ('category',)

class GroupCommentAdmin(admin.ModelAdmin):
    list_display = ('id','group','comment')
    list_filter = ('group',)

class ImageTestAdmin(ImageCroppingMixin,admin.ModelAdmin):
    pass

class MealParticipantsAdmin(admin.ModelAdmin):
    list_display = ('id', 'userprofile', 'meal')
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
    
class UserPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'photo')
    actions = ['resend_message']
    
    def resend_message(self, request, queryset):
        for up in queryset:
            photo_uploaded(UserPhoto, up, True)
        self.message_user(request, "成功发送用户上传照片消息!")

    resend_message.short_description = u"重新发送用户上传照片消息"
    
admin.site.register(Meal, MealAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(TransFlow, TransFlowAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(DishCategory, DishCategoryAdmin)
admin.site.register(Menu,MenuAdmin)
admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(UserTag)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(GroupCategory)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupComment, GroupCommentAdmin)
admin.site.register(ImageTest,ImageTestAdmin)
admin.site.register(MealParticipants, MealParticipantsAdmin)
admin.site.register(Relationship, RelationshipAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(UserPhoto, UserPhotoAdmin)

