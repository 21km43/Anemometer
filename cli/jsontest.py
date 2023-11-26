import requests
import json
import numpy as np
import time
import datetime

def sinwind(min):
    return 5*(np.sin(min/60*2*np.pi)+1)


url = "http://localhost:8000/data/create/"
sess = requests.session()

# ヘッダ
headers = {'Content-type': 'application/json',}


# POST送信
while(True):
    min=int(datetime.datetime.now().strftime('%M'))
    prm = {"WindSpeed":str(sinwind(min)),"AID":"1","Time":str(datetime.datetime.now())}
    params = json.dumps(prm)
    res = sess.post(url, data=params, headers=headers)
    # 戻り値を表示
    print("--戻り値----------------------------")
    print(res.text)


    min=-int(datetime.datetime.now().strftime('%M'))
    prm = {"WindSpeed":str(sinwind(min)),"AID":"2","Time":str(datetime.datetime.now())}
    params = json.dumps(prm)
    res = sess.post(url, data=params, headers=headers)
    # 戻り値を表示
    print("--戻り値----------------------------")
    print(res.text)


    time.sleep(1)
    