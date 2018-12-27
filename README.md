```
.
├── Dockerfile-serverless
├── docker-compose.yaml
├── README.md
├── .env
└── work
    ├── handler.py
    └── serverless.yaml
```
# What
Serverless Framework(in Docker)を利用して以下のlambdaファンクションをデプロイするやつ
・サイト公開に合わせ、特定のSecurity Groupに対して80/443ポートを全解放

※ Serverless in Docker部分は汎用のため、Dockerfile及びdocker-compose.yamlは流用可
# Usage
## 1. set env
.envファイルを編集
AWS_PROFILE及び発火タイミング(cron)・対象SGを指定

## 2. docker build (only first)
```
$ docker-compose build

# 引数なしで実行するとバージョン情報
$ docker-compose run --rm sls
1.35.1

# slsに続けて引数をそのまま追加してコマンド実行
$ docker-compose run --rm sls help

Commands
* You can run commands with "serverless" or the shortcut "sls"
* Pass "--verbose" to this command to get in-depth plugin info
.
.
.
```
## 3. deploy
.env以外に変更箇所なし。そのままデプロイ
```
$ docker-compose run --rm sls deploy -v
.
.
.
Service Information
service: add-sg-rule
stage: prd
region: ap-northeast-1
stack: add-sg-rule-prd
api keys:
  None
endpoints:
  None
functions:
  add-sg-rule: add-sg-rule-prd-add-sg-rule
layers:
  None
```
### 3-1. (piculet)
0.0.0.0/0のルールを足しているだけなので、
piculetやterraformなどでSG運用している場合は別途そちらの辻褄も合わせる。

## 4. remove
ロググループやiam含め、関連ファイルは全て消去される
```
$ docker-compose run --rm sls remove -v
.
.
.
Serverless: Stack removal finished...
```

# Tips
## 1. 変数の流れ
handler.py内の変数 `SGID`
  <- `SGID = os.environ['SGID']` としてLambda側設定の環境変数を参照
    <- serverless.yaml 上、 `SGID: ${env:SGID}` としてdockerコンテナ内の環境変数を参照
      <- docker-compose.yaml 上、コンテナ内の環境変数としてファイル: `.env` を参照

## 2. serverless createを利用したい時
path指定無しで作成すればwork配下にテンプレートファイルが作成されます
```
# 例
$ docker-compose run --rm sls create --template aws-nodejs --name myservice
Serverless: Generating boilerplate...
 _______                             __
|   _   .-----.----.--.--.-----.----|  .-----.-----.-----.
|   |___|  -__|   _|  |  |  -__|   _|  |  -__|__ --|__ --|
|____   |_____|__|  \___/|_____|__| |__|_____|_____|_____|
|   |   |             The Serverless Application Framework
|       |                           serverless.com, v1.35.1
 -------'

Serverless: Successfully generated boilerplate for template: "aws-nodejs"
$ ls work/
handler.js    serverless.yml
```
