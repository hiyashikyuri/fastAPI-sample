### 概要
FastAPIでシンプルなAPIを構築する際のテンプレとして作成しました。

### コマンド
```
# サーバー起動 / どちらでもいけます
python run.py

uvicorn app.main:app --reload

# migrationファイル生成
alembic revision -m "message" --autogenerate

# migration最新版適用
alembic upgrade head

```

### 内容
```
Python ver: 3.8
FastAPI ver: 
SQLAlchemy ver:
alembic 
```

### Lintやテスト
```
# テスト
pytest

# lint
flake8 app --max-line-length 120 --exclude main.py

```


### ライセンス
個人開発・商用利用問わずご自由にご活用ください。
また、利用する際はtwitterでのシェアや、引用として記載していただけますと幸いです。
※エラーや問題が発生して損失が出たとしても、

### 質問など
質問などありましたら、twitterにお願いします

twitter: https://twitter.com/masa_okubo
