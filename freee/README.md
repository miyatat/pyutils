## 手順
1. https://app.secure.freee.co.jp/developers/applications/ でアプリ作成
   - ClientID・ClientSecret・アプリのencodedコールバックURL取得
1. アプリケーションからredirect_uriを利用して認可コードを取得する or  ブラウザで認可コード取得する
   - appの下書き画面で見える
   - こんな感じのURL
   - https://accounts.secure.freee.co.jp/public_api/authorize?client_id=591524789919758&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&response_type=code&prompt=select_company
1. 認可コード
   - e4d7ec165b0aa138a720f222969e9a6ae7be3eb7cb8f34af3167a5279d8b5637
2. Access Token URLでアクセストークン取得
```bash
curl -i -X POST \
 -H "Content-Type:application/x-www-form-urlencoded" \
 -d "grant_type=authorization_code" \
 -d "client_id=アプリのClient ID" \
 -d "client_secret=アプリのClient Secret" \
 -d "code=取得した認可コード" \
 -d "redirect_uri=アプリのencodedコールバックURL" \
 "https://accounts.secure.freee.co.jp/public_api/token"
```

例）
```bash
curl -i -X POST \
 -H "Content-Type:application/x-www-form-urlencoded" \
 -d "grant_type=authorization_code" \
 -d "client_id=591524789919758" \
 -d "client_secret=ef320BoNNgbCxX0RCdcj5oSh65WIHmyc4h7HTayRQvY3DdDB7xippy1iOyKj1sCbGizTOVNJjoq1WNEBsJGWgQ" \
 -d "code=e4d7ec165b0aa138a720f222969e9a6ae7be3eb7cb8f34af3167a5279d8b5637" \
 -d "redirect_uri=urn:ietf:wg:oauth:2.0:oob" \
 "https://accounts.secure.freee.co.jp/public_api/token"
```
responce例）
```
{"access_token":"1f4a3637ffd3ff2860b648f7c5d295871f6142c3e4238444e8ed274f44a9396c","token_type":"bearer","expires_in":21600,"refresh_token":"7f81578272ab42cedc5035690d8343a96191a510c98728e61e5a41228fbd3608","scope":"default_read accounting:account_items:read accounting:approval_flow_routes:read accounting:companies:read accounting:deals:read accounting:docs:read accounting:expense_application_templates:read accounting:expense_applications:read accounting:approval_requests:read accounting:approval_request_forms:read accounting:payment_requests:read accounting:items:read accounting:manual_journals:read accounting:partners:read accounting:receipts:read accounting:reports_bs:read accounting:reports_journals:read accounting:reports_pl:read accounting:reports_cr:read accounting:sections:read accounting:tags:read accounting:taxes:read accounting:transfers:read accounting:users:read accounting:wallet_txns:read accounting:walletables:read","created_at":1752122803,"company_id":11605275,"external_cid":"7002194149"}
```
