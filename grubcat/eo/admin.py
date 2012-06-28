from django.contrib import admin
from eo.models import Restaurant, Dish, DishCategory, Order, Meal

class DishAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'name', 'price', 'unit', 'available',)
    list_editable = ('name', 'price', 'unit', 'available', )
    list_display_links = ('restaurant',)
    list_filter = ('restaurant',)
    ordering = ('restaurant',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('meal', 'customer', 'status', 'num_persons', 'total_price',)
    list_filter = ('meal', 'status')
    ordering = ('meal', 'status',)


class MealAdmin(admin.ModelAdmin):
    list_display = ('topic', 'restaurant','host', 'list_price','time')
    list_filter = ('restaurant',)
    ordering = ('restaurant', )

admin.site.register(Meal, MealAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Restaurant)
admin.site.register(Dish, DishAdmin)
#admin.site.register(DishCategory)