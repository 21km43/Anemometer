from rest_framework import serializers
from .models import Winddata

class UseWinddata(serializers.ModelSerializer):
    class Meta:
        model=Winddata
        fields='__all__'