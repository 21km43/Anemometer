from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters import rest_framework as filters

from django.views.decorators.csrf import csrf_exempt

import datetime,json,random,hashlib

from .models import Data
from .serializers import UseData

#TZ = datetime.timezone(datetime.timedelta(hours=+9), 'JST')


class LatestData():
    LHWD=[]#WindSpeed:,Time:(datetime型),AID
    Anemometer=[]#AID,Status,LastUpdate(datetime型)
    allKeys=[123,456,789]
    EmncriptedToken=[]

    def DataInit(self):#DBから過去データ抽出
        LHWD_query_set=Data.objects.all()
        self.LHWD=list(LHWD_query_set.values())
        self.checkLHWD()
        print('latestdata init')

    def syntax_check(self,givendata):
        data=json.loads(givendata)
        if 'WindSpeed' in data and 'Time' in data and 'AID' in data and 'EmcriptedToken' in data:
            return True
        else:
            return False

    def updateLHWD(self,givendata): 
        data=json.loads(givendata)
        data={"WindSpeed":data["WindSpeed"],"Time":datetime.datetime.strptime(data["Time"],"%Y-%m-%d %H:%M:%S.%f"),"AID":data["AID"]}
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
            if data['Time']<(datetime.datetime.now()-datetime.timedelta(hours=1)):
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

    def createToken(self):
        Token=random.randint(0,100000)
        et=[]
        for key in self.allKeys:
            et.append(hashlib.sha256((str(Token)+str(key)).encode()).hexdigest())
        self.EmncriptedToken.append(et)
        #print(self.EmncriptedToken)
        return Token

    def auth(self,EnToken):
        auth=False
        for i in range(len(self.EmncriptedToken)):
            for et in self.EmncriptedToken[i]:
                #print(et," ",EnToken,"does not match")
                if et==EnToken:
                    auth=True
                    tokenid=i
        if(auth):self.EmncriptedToken.remove(self.EmncriptedToken[tokenid])
        #print(self.EmncriptedToken)
        return auth


latestdata=LatestData() 


class WinddataFilter(filters.FilterSet):
    times=filters.DateTimeFilter()
    class Meta:
        model=Data
        fields='__all__'

class WinddataAPIView(APIView):

    def post(self,request):
        if not latestdata.syntax_check(request.body):
            return HttpResponse("Syntax Error")
        if not latestdata.auth(json.loads(request.body.decode('utf-8'))['EmcriptedToken']):
            return HttpResponse("Authentication Error")
        latestdata.updateLHWD(request.body)
        latestdata.updateAnemometer(request.body)
        DataSerializer=UseData(data=request.data)
        DataSerializer.is_valid(raise_exception=True)
        DataSerializer.save()
        return HttpResponse('good')

    """
    def get(self,request):
        latestdata.checkLHWD()
        filterset=WinddataFilter(request.query_params,queryset=Data.objects.all())
        serializer=UseData(instance=filterset.qs,many=True)
        return Response(serializer.data)
    """


class FilterdWD(APIView):
    # filterd wind data
    def get(self,request):
        qs=request.query_params
        try:
            
            datetime_rangea_split=qs["datetime_range"].split(',')
            print(datetime_rangea_split)
            dt_form="%Y-%m-%dT%H:%M:%S"
            start_date=datetime.datetime.strptime(datetime_rangea_split[0],dt_form)
            end_date=datetime.datetime.strptime(datetime_rangea_split[1],dt_form)
            print("start:",start_date,"end:",end_date)
            row_objects=list(Data.objects.filter(Time__range=(start_date,end_date)).values())
            return Response(row_objects)
        except ValueError as e:
            print("ERROR recipted parameter is not valid type",e)
            return HttpResponse("ERROR recipted parameter is not valid type",e)
        except KeyError as e:
            print("ERROR  no specified datetime parameter",e)
            return HttpResponse("ERROR  no specified datetime parameter",e)
 
class LHWD(APIView):
    def get(self,request):
        latestdata.checkLHWD()
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
            #リストの中から最新の物をld_aid_lastとして取得(1分経過は除外)
            ld_aid_last=ld_aid[0]
            is_there_datas=False
            for item in ld_aid:
                #最大値を見つける
                if ld_aid_last['Time']<item['Time'] and item['Time']>(datetime.datetime.now()-datetime.timedelta(seconds=120)):
                    ld_aid_last=item
                    is_there_datas=True
            if (is_there_datas):LDlist.append(ld_aid_last)
        return Response(LDlist)

class anemometer(APIView):
    def get(self,request):
        latestdata.checkAnemometer()    
        return Response(latestdata.Anemometer)
    
class DHCP(APIView):
    def get(self,request):
        latestdata.checkAnemometer()
        return Response(latestdata.DHCP())
    

class Token(APIView):
    def get(self,request):
        return Response({"Token":str(latestdata.createToken())})


class test(APIView):
    def post(self,request):
        #print(request.body.decode('utf-8'))
        return Response(latestdata.auth(request.body.decode('utf-8')))

    def get(self,request):  
        #print(hashlib.sha256(("1234abcd").encode()).hexdigest())
        return HttpResponse('good')




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
