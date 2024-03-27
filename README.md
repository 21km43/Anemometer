

## 秘密鍵について
anemometer_serverのディレクトリで32Byteの鍵をBase64として出力してください。OpenSSLで出力する例を以下に示します。
```bash
openssl rand -base64 32 > private_key
```
