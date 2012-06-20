from django.contrib import admin
from eo.models import Restaurant

class RestaurantAdmin(admin.ModelAdmin):
    pass
admin.site.register(Restaurant, RestaurantAdmin)