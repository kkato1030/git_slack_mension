# Git Slack Mention

Github内にてメンションがあるとSlackに通知してくれます

# 環境

下記環境にて作成

- Python3.7
- Node.js 12.13.0
- Serverless Framework 1.49.0

# 開発環境構築

## 1. Serverless Framework インストール

```
$ npm install
or
$ yarn
```

## 2. Python 環境構築
### 2-1. pipenv 利用時

```
$ pipenv install
```

### 2-2. その他仮想環境ツール利用時

環境作成後、以下コマンドにてパッケージをインストール

```
$ pip install -r requirements.txt
```

# デプロイ

## 1. 設定ファイルの作成

```
$ cp config.json.sample config.json
$ vi config.json  // お好みのエディタで開く
```

設定値は以下の通りです

| 設定名 | 概要 | 例 |
| -- | -- | -- |
| mension | @<Githubユーザー名>: <SlackユーザーID> | "@kkato1030": "U9ZEXXXX" |
| group | グループメンション先ID | SHBXXXXX |
| webhook_url | Slack通知先チャンネルのWebhook URL | https://hooks.slack.com/services/xxxxx |


## 2. デプロイ

デプロイ先 AWS 環境への CLI アクセスが可能な環境で以下を実行します
なお実行には Administrator 権限を推奨します

```
$ npx serverless deploy
```

この際、API Gateway のエンドポイントが表示されるため控えておいてください

## 3. Github の設定

Github にて Webhook の設定を行います
リポジトリの画面において以下を行ってください
1. [Settings] -> [Webhooks] を開き [Add webhook] を選択
2. 以下設定を行い、[Add webhook] を選択

| 設定名 | 設定値 |
| -- | -- |
| Payload URL | API Gateway のURL |
| Content type | application/json |
| Secret | (空欄) |
| Which events ... | Let me select individual events. |

イベントは以下の項目にチェックを入れることを推奨します

- Issue comments
- Issues
- Pull requests
- Pull requests reviews
Pull request review comments
