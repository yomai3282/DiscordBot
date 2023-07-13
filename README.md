- [環境構築メモ](#環境構築メモ)
  - [導入](#導入)
  - [ファイル構造](#ファイル構造)
  - [.env(環境変数の定義)](#env環境変数の定義)
  - [pipenv（ライブラリの管理）](#pipenvライブラリの管理)
  - [Docker（仮想環境の構築）](#docker仮想環境の構築)
  - [PostgreSQL（データベース）](#postgresqlデータベース)
- [よく使うコマンド](#よく使うコマンド)
  - [pipenv](#pipenv)
  - [Docker](#docker)
  - [PostgresSQL](#postgressql)
- [Raspberry Piに移植](#raspberry-piに移植)

# 環境構築メモ

DiscordのBotを作るにあたって、開発環境はwindows、本番環境はRaspberry Pi 4(Ubuntu 22.04)で動かせるようにしたい。

そこで、windowsでlinuxマシンを仮想的に動かせるwsl2と、簡単に仮想環境を構築できるDockerを利用した。

Dockerにはコンテナを２つ用意している。１つはDiscordBotを動かすためのコンテナ、もう１つはPostgreSQLというデータベースを動かすためのコンテナである。

これで、データベースから取得したデータをDiscordに投稿することができる。

## 導入

[Pythonで始める録音機能付きDiscord Bot: (1) 入門 discord.py - Qiita](https://qiita.com/Shirataki2/items/3b9f9766bc25bb204ed3)

このサイトを全体のベースとしている。Docker+pipenvでpythonの仮想環境を構築した。PostgreSQLをdockerで動かしているのは、購入した書籍がたまたまPostgreSQLに準拠したものだったから。

## ファイル構造

```c
DiscordBot //ターミナルのルート
├──.env //環境変数を定義するファイル
├── DiscordBot.code-workspace //vscodeのワークスペース
├── docker-compose.dev.yml //hihiiroとpostgreの起動設定
├── run.sh //コンテナをbuild・up・stopするとき使うショートカット
└── src //コンテナ内におけるルート(/botにマウントするフォルダ)
    ├── app
    │   ├── config.ini
    │   ├── entrypoint.dev.sh 
    │   ├── hihiiro 
    │   │   ├── cogs //botのコマンド集
    │   │   │   ├── Embed.py
    │   │   │   ├── Game.py
    │   │   │   ├── __init__.py
    │   │   │   └── __pycache__
    │   │   ├── core //botの起動時にコマンドをロード
    │   │   │   ├── bot.py
    │   │   │   ├── __init__.py
    │   │   │   └── __pycache__
    │   │   ├── __init__.py
    │   │   ├── __main__.py //botの起動
    │   │   └── __pycache__
    │   ├── Pipfile //pipenvで管理しているライブラリなどが書かれている
    │   └── Pipfile.lock
    ├── dev.dockerfile //docker起動時にターミナルで実行されるコマンド群
    └── psgl //PostgreSQLのデータ・接続設定
        ├── data
        │   ├──(省略)
    　  │   ├──pg_hba.conf //ユーザーのログイン設定など
        │   └──postgresql.conf //listen_addressesやportの設定など
        ├── init //postgresqlのコンテナ起動時に読み込まれる？らしい
        └── tmp
```
## .env(環境変数の定義)
DiscordBot/.env 内に環境変数を定義する。
```
TOKEN=...
DATABASE_URL=postgresql://{username}:{password}@{hostname}:{port}/{database}
```
動かしたいDiscordBotのトークン(TOKEN)やPostgreSQLのURL(DATABASE_URL)を書き込むので、公開するのはNG。

トークンの取得方法は、ここでは説明しない。

DATABASE_URLのhostnameは、コンテナ内で参照する場合は、postgresqlを動かしているコンテナであるmy_postgresがhostだが、コンテナ外から参照する場合はlocalhostになるので注意が必要。

## pipenv（ライブラリの管理）

### pythonバージョン：3.9

### discord.py

discordに関するライブラリ

### psycopg2-binary

pythonでPostgreSQLを操作するためのライブラリ

詳しくは以下の記事を参照

[PythonでPostgreSQLを操作する（psycopg2）](https://python-work.com/postgresql-psycopg2/)

## Docker（仮想環境の構築）

docker-composeで２つのコンテナを起動する。

### my_postgres

データベース(PostgreSQL)を起動するコンテナ

以下の記事を参考にdocker-compose.dev.ymlにmy_postgresの記述を追加した

[DockerでPostgreSQLを使う - Qiita](https://qiita.com/zaburo/items/7ab51a7a4d9e1b2d1ec4)

### hihiiro

DiscordBotを起動するコンテナ

## PostgreSQL（データベース）

postgresql 14のインストール・基本操作などは以下の記事を参照

[PostgreSQL 14, pgAdmin 4, PostGIS 3 のインストール（Ubuntu 上）](https://www.kkaneko.jp/tools/ubuntu/postgresql14.html)

### a5m2（データベースGUI）

GUIでデータベースを表示できるソフト。接続テストもできる。
a5m2を接続するためのpg_hba.confとpostgresql.confの設定は以下の記事を参照。
[WSL2+Ubuntu+PostgreSQL | のい太ろぐ](https://noitalog.tokyo/wsl2-ubuntu-postgresql/)

# よく使うコマンド

「○○があるディレクトリで～」と書かれていなければ、基本的にカレントディレクトリがDiscordBotの状態でコマンドを実行している。

## pipenv

### pipenv shell

Pipfileがあるディレクトリ(DiscordBot/src/app)で`pipenv shell`を実行すると、pipenv環境がactivateされる（仮想環境に入ると(app)と表示される）

仮想環境から抜けるときは`exit`する

### pipenv install {ライブラリ名}

Pipfileがあるディレクトリ(DiscordBot/src/app)で`pipenv install {ライブラリ名}`を実行すると、仮想環境にそのライブラリがインストールされる

アンインストールしたいときは`install`を`uninstall`に変える

## Docker

### sudo ./run.sh dev {build/up/stop/down}

build　コンテナをビルド（再構成）

up　コンテナを起動

up&　コンテナをバックグラウンドで起動

stop　コンテナを停止

down コンテナを削除

run.shの中身はこうなっている。

```bash
cmd="docker-compose -f docker-compose.$1.yml -p $1 ${@:2}"
echo $cmd
eval $cmd
```

要するに、`sudo ./run.sh dev {build/up/stop/down}`は

`sudo docker-compose -f docker-compose.dev.yml -p {build/up/stop/down}`と同じ。

### sudo docker ps [-a]

現在起動しているコンテナを表示する。

 [-a]オプションを付けた場合、停止したコンテナも表示される。

### sudo docker exec -it {コンテナ名} /bin/bash

{コンテナ名}が起動しているときに、コンテナの中身、つまり仮想環境に入るコマンド。仮想環境から抜けるときは`exit`する

### sudo chmod 777 -R src/psgl

docker-composeをbuildするとpsglの権限がセットされるので毎回権限を与えている。多分簡単に治せると思うが、めんどくさいので放置している。

psglディレクトリにあるpg_hba.confとpostgresql.confの設定を変えるときに使う。

## PostgresSQL

### PostgreSQLサーバーを起動

２つの方法がある。

1. ubuntuのターミナルから直接

`sudo pg_ctlcluster 14 main restart`

で起動

1. dockerのmy_postgreコンテナを起動(同時にhihiiroコンテナも起動する)

`sudo ./run.sh dev up`

### psql -h localhost -U  -{ユーザー名} -d {DB名}

postgresqlサーバーor my_postgreコンテナが起動している状態で、`psql -h localhost -U  -{ユーザー名} -d {DB名}`を実行すると、その{ユーザー名}に対応するパスワードの入力が要求されたのち、localhostのデータベースに{ユーザー名}としてログインし、{DB名}にアクセスできる

例：

`psql -h localhost -U postgres -d postgres`

`psql -h localhost -U testuser -d postgres`

※ラズパイがホストのときはラズパイのipアドレスを指定する。

データベースにアクセスした後は、sql文で操作を行う。

アクセスを終了するには`\q`を入力

PostgreSQLサーバーの再起動・終了・確認

1. ターミナルから直接起動したときは

`sudo pg_ctlcluster 14 main restart`で再起動、

`sudo pg_ctlcluster 14 main stop`で終了

`sudo pg_ctlcluster 14 main status`でステータスを確認

1. dockerのmy_postgreコンテナで起動したときは

`sudo ./run.sh dev down`で終了

PostgreSQLサーバーが終了していない状態で、`sudo ./run.sh dev up`（コンテナを起動）すると、エラーを吐くので、
一旦、`sudo pg_ctlcluster 14 main stop`するとよい。

# Raspberry Piに移植（ほかのデバイスでビルド）

1. このリポジトリをRaspberry Piの適当なディレクトリ(~/Documents/)などにgit clone

具体的な方法は以下の記事を参照。

[【GitHub】Deploy keysを使ってsshでpullするまで](https://qiita.com/tamorieeeen/items/c24f8285448b607b12dd)

3. `chmod 777 -R DiscordBot`で権限を付与
4. 3. DiscordBot/.envにDiscordBotのTOKENやPostgreSQLのDATABASE_URLなど、必要な環境変数を書き込む(`nano .env`)
5. `sudo ./run.sh dev build`,`sudo ./run.sh dev up`を試してみる。postgresのコンテナがエラーを吐いている場合、その内容に従って修正を行う。

## データベースの移植を行う場合

src/psgl/dataにpostgresqlのmainディレクトリを移植する。linuxの場合は、/etc/postgresql/14/mainに保存されているはず。

5. FATAL:  could not open directory "pg_notify": No such file or directoryなどと表示される場合、src/psgl/data/に不足しているファイル・ディレクトリを作成する。
- pg_notify
- pg_tblspc
- pg_replslot
- pg_twophase
- pg_commit_ts
- pg_stat_tmp/global.tmp
- pg_snapshots
- pg_logical/snapshots
- pg_logical/pg_snapshots
- pg_logical/mappings

## データベースをすべて新規で作成する場合

5. そのまま`sudo ./run.sh dev {build/up}`しても接続できない。

おそらくpsglディレクトリにあるpg_hba.confとpostgresql.confの設定を変える必要がある。

まずpostgresqlをラズパイにインストールして、ラズパイ上で動作を確認する。

[PostgreSQL 14, pgAdmin 4, PostGIS 3 のインストール（Ubuntu 上）](https://www.kkaneko.jp/tools/ubuntu/postgresql14.html)

今の所こんな感じ↓の設定で動いている

pg_hba.conf
```bash
# Database administrative login by Unix domain socket
local    all            postgres                                md5
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
#local   all             all                                     peer
# IPv4 local connections:
host    all             all               all                     md5
#host     all             all             all                     md5
# IPv6 local connections:
host    all             all             ::1/128                 scram-sha-256
# Allow replication connections from localhost, by a user with the
# replication privilege.
local   replication     all                                     peer
host    replication     all             127.0.0.1/32            scram-sha-256
host    replication     all             ::1/128                 scram-sha-256
local   all             all                                     md5
```

postgresql.conf
```bash
listen_addresses = '0.0.0.0'
port = 5432
```

6. 別のデバイスからDBに接続できれば移植完了!
