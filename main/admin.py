from django.contrib import admin
from main.models import Services

# Register your models here.

class ServicesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Services, ServicesAdmin)