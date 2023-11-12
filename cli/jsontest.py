import requests
import json

url = "http://localhost:8000/data/posttest/"
sess = requests.session()



# ヘッダ
headers = {'Content-type': 'application/json',}

# 送信データ
prm = {"param1": "パラメータ１", "param2": "パラメータ２"}

# JSON変換
params = json.dumps(prm)

# POST送信
res = sess.post(url, data=params, headers=headers)

# 戻り値を表示
print("--戻り値----------------------------")
print(res.text)
print(json.loads(res.text))