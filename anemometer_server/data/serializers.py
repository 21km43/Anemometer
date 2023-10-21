from rest_framework import serializers
from .models import Winddata, Anemometor

class UseWinddata(serializers.ModelSerializer):
    class Meta:
        model=Winddata
        fields = '__all__'

class UseAnemometor(serializers.ModelSerializer):
    class Meta:
        model = Anemometor
        fields = '__all__'