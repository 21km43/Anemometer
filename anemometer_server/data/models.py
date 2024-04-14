from django.db import models
# Create your models here.
from django.utils import timezone


class Data(models.Model):
    Time=models.DateTimeField()
    AID=models.IntegerField()
    data=models.JSONField()