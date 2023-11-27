from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters import rest_framework as filters

from django.views.decorators.csrf import csrf_exempt

import datetime,json

from .models import Data
from .serializers import UseData

class LatestData():
    LHWD=[]#WindSpeed:,Time:,AID
    Anemometer=[]#AID,Status,LastUpdate
    Token=[]

    def __init__(self):#DBから過去データ抽出
        print('latestdata init')

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
        exist_anemometer=False
        for data in self.Anemometer:
            if str(data['AID'])==str(AID):
                exist_anemometer=True
                data['Status']='Working'
                data['LastUpdate']=str(datetime.datetime.now())
        if not exist_anemometer:
            self.Anemometer.append({"AID":AID,"Status":"Working","LastUpdate":str(datetime.datetime.now())})

    def checkLHWD(self):
        rmlist=[]
        for data in self.LHWD:
            if datetime.datetime.strptime(data['time'],'%Y-%m-%d %H:%M:%S.%f')< datetime.datetime.now()-datetime.timedelta(hours=1):
                rmlist.append(data)
        for data in rmlist:
            self.LHWD.remove(data)

    def checkAnemometer(self):
        rmlist=[]
        for data in self.Anemometer:
            if datetime.datetime.strptime(data['LastUpdate'],'%Y-%m-%d %H:%M:%S.%f')<(datetime.datetime.now()-datetime.timedelta(seconds=15)):
                self.Anemometer[self.Anemometer.index(data)]['Status']='Unstable'
            if datetime.datetime.strptime(data['LastUpdate'],'%Y-%m-%d %H:%M:%S.%f')<(datetime.datetime.now()-datetime.timedelta(seconds=60)):
                rmlist.append(data)
        for data in rmlist:
            self.Anemometer.remove(data)

    def DHCP(self):
        for i in range(100):
            flag=True
            for data in self.Anemometer:
                if data['AID']==str(i+1):
                    flag=False
            if flag:return {"AID":i+1}
        print('DHCP error')


latestdata=LatestData()


class WinddataFilter(filters.FilterSet):
    class Meta:
        model=Data
        fields='__all__'

class WinddataAPIView(APIView):

    def post(self,request):
        if not latestdata.syntax_check(request.body):
            return HttpResponse("Syntax Error")
        latestdata.updateLHWD(request.body)
        latestdata.updateAnemometer(request.body)
        DataSerializer=UseData(data=request.data)
        DataSerializer.is_valid(raise_exception=True)
        DataSerializer.save()
        return HttpResponse('good')

    def get(self,request):
        latestdata.checkLHWD()
        filterset=WinddataFilter(request.query_params,queryset=Data.objects.all())
        serializer=UseData(instance=filterset.qs,many=True)
        return Response(serializer.data)

 
class LHWD(APIView):
    def get(self,request):
        return Response(latestdata.LHWD)

class LD(APIView):
    def get(self,response):
        AIDset=[]
        LDlist=[]
        for item in latestdata.Anemometer:
            AIDset.append(item['AID'])
        #あるAIDを持つ要素の中から時間が最大の要素を返す関数を実装する(1分経過したものは非対称)         
        for aid in AIDset:
            ld_aid=[]                         
            #特定のAIDの物をリスとして準備
            for item in latestdata.LHWD:
                if item['AID']==aid:
                    ld_aid.append(item)
            ld_aid_last=ld_aid[0]
            #リストの中から最新の物をld_aid_lastとして取得(1分経過は除外)
            for item in ld_aid:
                if datetime.datetime.strptime(ld_aid_last['Time'],'%Y-%m-%d %H:%M:%S.%f')<datetime.datetime.strptime(item['Time'],'%Y-%m-%d %H:%M:%S.%f') and datetime.datetime.strptime(ld_aid_last['Time'],'%Y-%m-%d %H:%M:%S.%f')>(datetime.datetime.now()-datetime.timedelta(seconds=120)):
                    ld_aid_last=item
            LDlist.append(ld_aid_last)
        return Response(LDlist)

class anemometer(APIView):
    def get(self,request):
        latestdata.checkAnemometer()    
        return Response(latestdata.Anemometer)
    
class DHCP(APIView):
    def get(self,request):
        latestdata.checkAnemometer()
        return Response(latestdata.DHCP())


class test(APIView):
    def get(self,request):
        return Response([{"key":1,"data":2},{"key":2,"data":31}])










from django.http.response import JsonResponse
@csrf_exempt
def posttest(request):
    if request.method == 'GET':
            return Response({})

    # JSON文字列
    print(request.body)
    datas = json.loads(request.body)

    print("--受取り値--------------------------")
    print(type(datas))
    print(datas)

    # requestには、param1,param2の変数がpostされたものとする
    ret = {"data": "param1:" + datas["param1"] + ", param2:" + datas["param2"]}

    # JSONに変換して戻す
    return JsonResponse(ret)
