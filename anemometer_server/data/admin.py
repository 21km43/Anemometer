from django.contrib import admin

# Register your models here.

from .models import Data

@admin.register(Data)
class Winddata(admin.ModelAdmin):
    pass
