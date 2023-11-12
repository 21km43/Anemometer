from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters import rest_framework as filters

from django.views.decorators.csrf import csrf_exempt

import datetime,json

from .models import Winddata
from .serializers import UseWinddata

class LatestData():
    LHWD=[]#WindSpeed:,Time:,AID
    Anemometer=[]#AID,Status,LatestUpdate
    Token=[]

    def __init__(self):#DBから過去データ抽出
        print('latestdata init')

    def syntax_check(self,givendata):
        print(type(givendata))
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
            if data['AID']==AID:
                exist_anemometer=True
                data['Status']='Working'
                data['LastUpdate']=datetime.now()
        if not exist_anemometer:
            self.Anemometer()

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


latestdata=LatestData()


class WinddataFilter(filters.FilterSet):
    class Meta:
        model=Winddata
        fields='__all__'

class WinddataAPIView(APIView):

    def post(self,request):
        print('----------------------------')
        print(str(request.body.decode('utf-8')))
        print(type(json.loads(request.body)))
        print('----------------------------')
        #if not latestdata.syntax_check(request.body):
        #    return HttpResponse("Syntax Error")
        print('syntax check done')
        latestdata.updateLHWD(request.body)
        print('update done')
        #latestdata.updateAnemometer(request.data)
        print('update anemometer done')
        DataSerializer=UseWinddata(data=request.data)
        DataSerializer.is_valid(raise_exception=True)
        DataSerializer.save()
        return HttpResponse('good')

    def get(self,request):
        latestdata.checkLHWD()
        filterset=WinddataFilter(request.query_params,queryset=Winddata.objects.all())
        serializer=UseWinddata(instance=filterset.qs,many=True)
        return Response(serializer.data)

 
class LHWD(APIView):
    def get(self,request):
        return Response(latestdata.LHWD)

class LD(APIView):
    def get(self,response):
        data=latestdata.Anemometer
        AIDset=set()
        for item in data:
            AIDset.add(item["AID"])
        #あるAIDを持つ要素の中から時間が最大の要素を返す関数を実装する         
               



        return HttpResponse("good")

class anemometer(APIView):
    def get(self,request):
        return Response(latestdata.Anemometer)
    
class DHCP(APIView):
    def get(self,request):
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

testjson={"key":1,"data":2}
print(testjson)