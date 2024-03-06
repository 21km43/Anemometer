from django.shortcuts import render

# Create your views here.

import requests,json,datetime,time
from apscheduler.schedulers.background import BackgroundScheduler

from rest_framework.response import Response
from rest_framework.views import APIView

url="https://optimalis-database-default-rtdb.asia-southeast1.firebasedatabase.app/.json"
sess=requests.session()


class LatestData():
    LHWD=[]#WindSpeed:,Time:(datetime型),AID

    def updateLHWD(self,givendata): 
        self.LHWD.append(givendata)
    
    def checkLHWD(self):
        rmlist=[]
        for data in self.LHWD:
            if data['Time']<(datetime.datetime.now()-datetime.timedelta(hours=1)):
                rmlist.append(data)
        for data in rmlist:
            self.LHWD.remove(data)
    

fetch_fd=False
fetch_fd=True
latestdata=LatestData()

def get():
    if not fetch_fd:
        return 0
    get=sess.get(url) 
    json_data=json.loads(get.text)
    json_data['Time']=datetime.datetime.now()
    latestdata.updateLHWD(json_data)
    print("update")

def start():
   scheduler=BackgroundScheduler()

   scheduler.add_job(get,'interval',seconds=5)
   scheduler.start()



class LHWD(APIView):
    def get(self,response):
        latestdata.checkLHWD()
        return Response(latestdata.LHWD)