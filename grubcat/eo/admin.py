#coding=utf-8
from ajax_select.admin import AjaxSelectAdmin
import datetime
from django.contrib import admin
from image_cropping.admin import ImageCroppingMixin
from eo.models import Restaurant, Dish, DishCategory, Order, Meal, Menu, UserTag, DishItem, DishCategoryItem, GroupComment
from models import Group, GroupCategory, UserProfile, ImageTest

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','name','weibo_id','avatar')
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
    list_display = ('id','meal', 'customer', 'created_time','completed_time','status', 'num_persons', 'code','total_price',)
    list_filter = ('meal', 'status')
    ordering = ('-id','meal', 'status',)
    actions = ['cancel_order']
    def cancel_order(self, request, queryset):
        for order in queryset:
            order.cancel()
        self.message_user(request, "订单取消成功!")
    cancel_order.short_description = u"取消订单"


class MealAdmin(admin.ModelAdmin):
    list_display = ('topic', 'menu','host', 'list_price',)
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

class MenuAdmin(admin.ModelAdmin):
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


#admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(Order, OrderAdmin)
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

