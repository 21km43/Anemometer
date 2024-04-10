
### Start 
```bash
chmod +x init.sh
./init.sh
```

### Dockerコマンドで始める
コンテナを起動する
```bash
docker compose up -d
```
MySQLコンテナが起動するのに時間がかかるので、しばらく待ってからDBマイグレーションを行う
```bash
docker compose exec django chmod +x ./manage.py
docker compose exec django ./manage.py makemigrations
docker compose exec django ./manage.py migrate
docker compose exec djangp ./manage.py collectstatic --noinput
```

### 設定ファイルなどの変更を適用する
Volumeで紐づけられているソースコードなどはファイルを保存しただけで変更される
一部の設定ファイルが適用されない場合は以下のコマンドでファイルを強制的に転送して適用させる
```bash
docker compose down
docker compose build
docker compse up -d
```
