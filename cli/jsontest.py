import requests
import json
import numpy as np
import time
import datetime
import hashlib

def sinwind(min):
    return 5*(np.sin(min/60*2*np.pi)+1)


url = "http://localhost:8000/data/create/"  
sess = requests.session()



# ヘッダ
headers = {'Content-type': 'application/json',}



# POST送信
while(True):

    res=sess.get('http://localhost:8000/data/token/')
    giventoken=eval(json.loads(res.text))["Token"]

    min=int(datetime.datetime.now().strftime('%M'))
    prm = {"WindSpeed":str(sinwind(min)),"AID":"1","Time":str(datetime.datetime.now()),"EmcriptedToken":str(hashlib.sha256((giventoken+"123").encode()).hexdigest())}
    params = json.dumps(prm)
    res = sess.post(url, data=params, headers=headers)
    # 戻り値を表示
    print("--return body-----")
    print(res.text)

    time.sleep(1)
    