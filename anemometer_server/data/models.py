from django.db import models

# Create your models here.


class Winddata(models.Model):
    WindSpeed = models.FloatField()
    Time = models.DateTimeField()
    LHWD = models.BooleanField(default=True)
    LD = models.BooleanField(default=True)
    AID = models.IntegerField(default=0)

class Anemometor(models.Model):
    AID = models.IntegerField(default=0)
    Status = models.CharField(max_length=10)
    LastUpdate = models.DateTimeField()