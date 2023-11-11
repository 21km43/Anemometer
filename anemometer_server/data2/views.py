from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters import rest_framework as filters

import datetime,json

from .models import Winddata
from .serializers import UseWinddata

class LatestData():
    LHWD=[]#WindSpeed:,Time:,AID
    Anemometer=[]#AID,Status,LatestUpdate
    Token=[]

    def __init__(self):#DBから過去データ抽出
        print('init done')

    def syntax_check(self,givendata):
        data=json.loads(givendata)
        if 'WindSpeed' in data and 'Time' in data and 'AID' in data:
            return True
        else:
            return False

    def updateLHWD(self,givendata):
        data=json.loads(givendata)
        self.LHWD.append(data)
    
    def updateAnemometer(self,givendata):
        AID=json.loads(givendata)['AID']
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


class WinddataFilter(filters.FilterSet):
    class Meta:
        model=Winddata
        fields='__all__'

class WinddataAPIView(APIView):

    def post(self,request):
        if not LatestData.syntax_check(request.data):
            return HttpResponse("Syntax Error")
        LatestData.updateLHWD(json.load(request.data))
        LatestData.updateAnemometer(request.data)
        DataSerializer=UseWinddata(data=request.data)
        DataSerializer.is_valid(raise_exception=True)
        DataSerializer.save()
        return HttpResponse('good')

    def get(self,request):
        LatestData.checkLHWD()
        filterset=WinddataFilter(request.query_params,queryset=Winddata.objects.all())
        serializer=UseWinddata(instance=filterset.qs,many=True)
        return Response(serializer.data)

 
class LHWD(APIView):
    def get(self,request):
        return Response(LatestData.LHWD)

class LD(APIView):
    def get(self,response):
        data=LatestData.Anemometer
        AIDset=set()
        for item in data:
            AIDset.add(item["AID"])
        #あるAIDを持つ要素の中から時間が最大の要素を返す関数を実装する         
               



        return HttpResponse("good")

class anemometer(APIView):
    def get(self,request):
        return Response(LatestData.Anemometer)

class test(APIView):
    def get(self,request):
        return Response([{"key":1,"data":2},{"key":2,"data":31}])