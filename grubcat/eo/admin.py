#coding=utf-8
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
from django.contrib import admin
from eo.models import Restaurant, Dish, DishCategory, Order, Meal

class DishAdmin(AjaxSelectAdmin):
#    form = make_ajax_form(Dish,{'categories':'dish_category'})
    list_display = ('restaurant', 'name', 'price', 'unit', 'available',)
    list_editable = ('name', 'price', 'unit', 'available', )
    list_display_links = ('restaurant',)
    list_filter = ('restaurant',)
    ordering = ('restaurant',)

class DishCategoryAdmin(admin.ModelAdmin):
    pass

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
    list_display = ('topic', 'restaurant','host', 'list_price','time')
    list_filter = ('restaurant',)
    ordering = ('restaurant', )

admin.site.register(Meal, MealAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Restaurant)
admin.site.register(Dish, DishAdmin)
admin.site.register(DishCategory, DishCategoryAdmin)
#admin.site.register(DishCategory)