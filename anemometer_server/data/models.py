from django.db import models
# Create your models here.
from django.utils import timezone


class Data(models.Model):
    WindSpeed=models.FloatField(default=0)
    WindDirection=models.FloatField(default=0)
    Time=models.DateTimeField()
    AID=models.IntegerField()
    Memo=models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )