import requests
import json
import numpy as np
import time
import datetime
import hashlib
import hmac
import base64

def sinwind(min):
    return 5*(np.sin(min/60*2*np.pi)+1)


url = "http://localhost:8000/data/create/"  
sess = requests.session()


# POST送信
while(True):

    res=sess.get('http://localhost:8000/data/token/')
    giventoken=eval(json.loads(json.dumps(res.text)))["Token"]

    min=int(datetime.datetime.now().strftime('%M'))
    prm = {
        "WindSpeed":str(sinwind(min)),
        "WindDirection":"0",
        "Longitude":"0",
        "Latitude":"0",
        "Memo":"滑走路　南",
        "AID":"1",
        "Time":str(datetime.datetime.now())}
    params = json.dumps(prm)
    # HMAC-SHA256（BASE64符号）を計算
    signature = hmac.new(b'123', params, hashlib.sha256).hexdigest()
    signature_base64 = base64.b64encode(signature).decode()
    # HTTPヘッダ
    headers = {'Content-type': 'application/json', 'Autherization': signature_base64}
    res = sess.post(url, data=params, headers=headers)
    # 戻り値を表示
    print("--return body-----")
    print(res.text)

    time.sleep(1)
    