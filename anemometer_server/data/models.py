from django.db import models

# Create your models here.

class Data(models.Model):
    WindSpeed=models.FloatField()
    
    Time=models.DateTimeField()
    AID=models.IntegerField()