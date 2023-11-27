from django.db import models
# Create your models here.
from django.utils import timezone


class Data(models.Model):
    WindSpeed=models.FloatField(default=timezone.now)
    
    Time=models.DateTimeField()
    AID=models.IntegerField()