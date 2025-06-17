from django.contrib import admin
from main.models import Services, Order

# Register your models here.

class ServicesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Services, ServicesAdmin)


class OrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Order, OrderAdmin)