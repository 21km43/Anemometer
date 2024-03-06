import requests
import json
import numpy as np
import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler

url="https://optimalis-database-default-rtdb.asia-southeast1.firebasedatabase.app/.json"
sess=requests.session()

def get():
   get=sess.get(url) 
   print(get.text)
   json_data=json.loads(get.text)
   json_data['Time']=str(datetime.datetime.now())
   print(json_data)

def start():
   scheduler=BackgroundScheduler()

   scheduler.add_job(get,'interval',seconds=0.5)
   scheduler.start()


start()

time.sleep(1000)