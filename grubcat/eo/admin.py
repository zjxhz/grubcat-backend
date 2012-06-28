#coding=utf-8
from django.contrib import admin
from eo.models import Restaurant, Dish, DishCategory, Order, Meal

class DishAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'name', 'price', 'unit', 'available',)
    list_editable = ('name', 'price', 'unit', 'available', )
    list_display_links = ('restaurant',)
    list_filter = ('restaurant',)
    ordering = ('restaurant',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','meal', 'customer', 'created_time','status', 'num_persons', 'total_price',)
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
#admin.site.register(DishCategory)