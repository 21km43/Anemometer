
### Start 
```bash
chmod +x init.sh
./init.sh
```

### Dockerコマンドで始める
コンテナを起動する。もしくは再起動する
```bash
docker compose up -d
docker compose restart
```
MySQLコンテナが起動するのに時間がかかるので、しばらく待ってからDBマイグレーションを行う
```bash
docker compose exec django chmod +x ./manage.py
docker compose exec django ./manage.py makemigrations
docker compose exec django ./manage.py migrate
docker compose exec djangp ./manage.py collectstatic --noinput
```
Windowsの場合のコマンドは次のようになる
```bash
docker compose exec django /bin/bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
exit
```
makemigrationsの途中で求められる値には`{}`を入れる。

### 設定ファイルなどの変更を適用する
Volumeで紐づけられているソースコードなどはファイルを保存しただけで変更される
一部の設定ファイルが適用されない場合は以下のコマンドでファイルを強制的に転送して適用させる
```bash
docker compose down
docker compose build
docker compose up -d
```


### 事前共有鍵を設定する
PSKを設定するためにはDjango管理画面を使用するので、管理ユーザーを作成する
```bash
docker compose exec django ./manage.py createsuperuser
```
Windowsの場合次の通り
```
docker compose exec django /bin/bash
python manage.py createsuperuser
```

http://HOSTNAME/adminにアクセスし、
DATA＞Secret Keyにて、右上の"Secret Keyを追加"ボタンを押下、任意の文字列を保存する。

現在、管理画面で複数のSecretKeyを保存することができるが、実際に適用されるのは最初に追加した一つだけである。
