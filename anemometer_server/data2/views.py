from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters import rest_framework as filters
import datetime

import json

from .models import Winddata
from .serializers import UseWinddata

class LatestData():
    LHWD=[]#WindSpeed:,Time:,AID
    Anemometer=[]#AID,Status,LatestUpdate

    def __init__(self):
        print('init done')

    def syntax_check(self,data):
        if 'WindSpeed' in data and 'Time' in data and 'AID' in data:
            return True
        else:
            return False

    def updateLHWD(self,data):
        self.LHWD.append(data)
    
    def updateAnemometer(self,AID):
        for data in self.Anemometer:
            if data['AID']==AID:
                data['Status']='Working'
                data['LastUpdate']=datetime.now()

    def checkLHWD(self):
        rmlist=[]
        for data in self.LHWD:
            if datetime.datetime.strptime(data['time'])< datetime.now()-datetime.timedelta(hours=1):
                rmlist.append(data)
        for data in rmlist:
            self.LHWD.remove(data)

    def checkAnemometer(self):
        rmlist=[]
        for data in self.Anemometer:
            if datetime.datetime.strptime(data['LastUpdate'])<datetime.now()-datetime.timedelta(seconds='15'):
                self.Anemometer[self.Anemometer.index(data)]['status']='unstable'
            if datetime.datetime.strptime(data['LastUpdate'])<datetime.now()-datetime.timedelta(seconds='60'):
                rmlist.append(data)
        for data in rmlist:
            self.Anemometer.remove(data)

    def DHCP(self):
        for i in range(100):
            flag=True
            for data in self.Anemometer:
                if data['AID']==str(i+1):
                    flag=False
            if flag:return i+1
        print('DHCP error')


class WinddataFilter(filters.filterset):
    class Meta:
        model=Winddata
        fields='__all__'

class WinddataAPIView(APIView):

    def post(self,request):
        if not LatestData.syntax_check(request.data):
            return HttpResponse("Syntax Error")
        LatestData.updateLHWD(json.load(request.data))
        DataSerializer=UseWinddata(data=request.data)
        DataSerializer.is_valid(raise_exception=True)
        DataSerializer.save()
        return HttpResponse('good')

    def get(self,request):
        filterset=WinddataFilter(request.query_params,queryset=Winddata.objects.all())
        serializer=UseWinddata(instance=filterset.qs,many=True)
        return Response(serializer.data)