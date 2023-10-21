from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters import rest_framework as filters
from django.utils import timezone


from .serializers import UseWinddata,UseAnemometor
from .models import Winddata,Anemometor

def FlagUpdater(getAID=0,update=False):
    #最新のデータにフラグを立てる。(LDは風速計ごとに一つ立てる)
    #データアップデートがあれば、前回データをLD=Falseにし、anemometor.status=workingにする
    if update :
        OutTimeLD=Winddata.objects.filter(LD=True,AID=getAID)
        OutTimeLD.update(LD=False)    
        try:
            anemometor=Anemometor.objects.get(AID=getAID)
            anemometor.Status='Working'
            anemometor.LastUpdate=timezone.now()
        except Anemometor.DoesNotExist:
            anemometor=Anemometor(AID=1,Status='Working',LastUpdate=timezone.now())
        anemometor.save()
    #Anemometorがworking or unstableで無ければLD=Falseにする
    OutAnemoLD=Winddata.objects.filter(LD=True)
    for record in OutAnemoLD:
        if not Anemometor.objects.filter(AID=record.AID).exists():
            anemometor=Winddata.objects.get(AID=record.AID,LD=True)
            anemometor.LD=False
            anemometor.save()
    #LHWD=TrueでなければLDもLD=Falseとする
    OutLHWDLD=Winddata.objects.filter(LD=True,LHWD=False)
    OutLHWDLD.update(LD=False)

    #latest one hour wind dataのフラグ更新
    OutTimeLHWD=Winddata.objects.filter(LHWD=True,Time__lte=timezone.now()-timezone.timedelta(hours=1))
    OutTimeLHWD.update(LHWD=False)
    InTimeLHWD=Winddata.objects.filter(LHWD=False,Time__gt=timezone.now()-timezone.timedelta(hours=1))
    InTimeLHWD.update(LHWD=True)


def avarage():
    ROWData=Winddata.objects.filter(LHWD=True)
    total_number=100
    part_number=int(ROWData.count()/100)
    windspeed_array=[]
    for i in range(total_number):
        avarage_speed=0
        #for j in range(part_number-2):
            #avarage_speed+=ROWData[i*100+j].WindSpeed
        avarage_speed/=part_number            
        windspeed_array.append({'WindSpeed':avarage_speed,'Time':ROWData[i*100].Time})
    return windspeed_array



class WinddataAPIView(APIView):
    def post(self, request, *args, **kwargs):
        DataSerializer = UseWinddata(data=request.data)
        DataSerializer.is_valid(raise_exception=True)
        FlagUpdater(DataSerializer.validated_data['AID'],True)     
        DataSerializer.save()
        return Response("saved")

class WinddataFilter(filters.FilterSet):
    class Meta:
        model = Winddata
        fields = '__all__'

class listdata(APIView):
    def get(self, request):
        FlagUpdater(update=False)
        filterset=WinddataFilter(request.query_params, queryset=Winddata.objects.all())
        serializer = UseWinddata(instance=filterset.qs, many=True)
        #avarage()
        return Response(serializer.data)

class AnemometorFilter(filters.FilterSet):
    class Meta:
        model = Anemometor
        fields = '__all__'

def AnemometorFlagUpdater():
    UnstableAnemometor=Anemometor.objects.filter(LastUpdate__lte=timezone.now()-timezone.timedelta(seconds=30))
    UnstableAnemometor.update(Status='Unstable')
    StoppingAnemometor=Anemometor.objects.filter(LastUpdate__lte=timezone.now()-timezone.timedelta(minutes=3))
    StoppingAnemometor.delete()

    return True

class AnemometorAIPView(APIView):
    def get(self,request):
        AnemometorFlagUpdater()
        filterset=AnemometorFilter(request.query_params, queryset=Anemometor.objects.all())
        serializer=UseAnemometor(instance=filterset.qs,many=True)
        return Response(serializer.data)

class DHCP(APIView):
    def get(self,request):
        for i in range(100):
            try:Anemometor.objects.get(AID=i+1)
            except Anemometor.DoesNotExist:
                return Response(i+1)
        return False

