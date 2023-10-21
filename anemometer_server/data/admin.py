from django.contrib import admin

# Register your models here.

from .models import Winddata,Anemometor

@admin.register(Winddata)
class Winddata(admin.ModelAdmin):
    pass


@admin.register(Anemometor)
class Anemometor(admin.ModelAdmin):
    pass