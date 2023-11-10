from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters import rest_framework as filters

import json

from .models import Winddata
from .serializers import UseWinddata

class LatestData():
    LHWD=[{}]#WindSpeed:,Time:,AID
    Anemometer=[{}]#AID,Status,LatestUpdate

    def __init__(self):
        print('init done')

    def syntax_check():
        return True

    def save(self,data):
        self.LHWD.append(data)

    def DHCP(self):
        return 1


class WinddataFilter(filters.filterset):
    class Meta:
        model=Winddata
        fields='__all__'

class WinddataAPIView(APIView):

    def post(self,request):
        if not LatestData.syntax_check(request.data):
            return HttpResponse("Syntax Error")
        LatestData.save(jason.load(request.data))
        DataSerializer=UseWinddata(data=request.data)
        DataSerializer.is_valid(raise_exception=True)
        DataSerializer.save()
        return HttpResponse('good')

    def get(self,request):
        filterset=WinddataFilter(request.query_params,queryset=Winddata.objects.all())
        serializer=UseWinddata(instance=filterset.qs,many=True)
        return Response(serializer.data)