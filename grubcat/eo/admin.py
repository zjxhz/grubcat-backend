from django.contrib import admin
from eo.models import Restaurant, Dish, DishTag, DishCategory

class DishAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'name','price','unit','available','is_recommended',)
    list_editable = ('name','price','unit','available','is_recommended',)
    list_display_links =('restaurant',)
    list_filter = ('restaurant',)
    ordering = ('restaurant',)

    def queryset(self, request):
        qs = super(DishAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(restaurant=request.user.restaurant)
admin.site.register(Restaurant)
admin.site.register(Dish, DishAdmin)
#admin.site.register(DishTag)
#admin.site.register(DishCategory)