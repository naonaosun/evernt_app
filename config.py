import datetime
from flask_login import UserMixin
from peewee import (
    SqliteDatabase,
    Model,
    IntegerField,
    IntegrityError,
    CharField,
    TextField,
    TimestampField,
    ForeignKeyField,
    DateTimeField,
)
from playhouse.migrate import SqliteMigrator, migrate


# SQLiteデータベースの設定
db = SqliteDatabase("db.sqlite")
db.connect()  # データベースに接続

# # マイグレーターの設定
# migrator = SqliteMigrator(db)

# # トランザクションを開始してマイグレーションを実行
# with db.atomic():
#     migrate(
#         migrator.add_column('events', 'start_date', DateTimeField(null=True)),
#         migrator.add_column('events', 'end_date', DateTimeField(null=True))
#     )


class User(UserMixin, Model):
    id = IntegerField(primary_key=True)
    name = CharField(unique=True)
    email = CharField(unique=True)
    password = TextField()

    class Meta:
        database = db
        table_name = "users"


class Event(Model):
    name = CharField()
    content = TextField(null=True)
    start_date = DateTimeField(null=True)
    end_date = DateTimeField(null=True)
    place = CharField()
    address = CharField()
    url = CharField(null=True)
    image = CharField(null=True)  # 画像ファイル名を保存するフィールド

    class Meta:
        database = db
        table_name = "events"

#★detaフィールドの削除★1～5を順を追って実行
## 1. 一時テーブルを作成し、データをコピー
# db.execute_sql('''
#     CREATE TABLE IF NOT EXISTS events_backup AS SELECT 
#     name, content, start_date, end_date, place, address, url, image 
#     FROM events;
# ''')

## 2. 元のテーブルを削除
# db.execute_sql('DROP TABLE events;')

## 3. 新しいスキーマでテーブルを作成
# db.create_tables([Event])

## 4. データを一時テーブルから新しいテーブルにコピー
# db.execute_sql('''
#     INSERT INTO events (name, content, start_date, end_date, place, address, url, image)
#     SELECT name, content, start_date, end_date, place, address, url, image FROM events_backup;
# ''')

# # 5. 一時テーブルを削除
# db.execute_sql('DROP TABLE events_backup;')






# def save(self, *args, **kwargs):
#     # バリデーションチェック
#     if self.start_date > self.end_date:
#         raise ValueError("Start date must be before end date.")

#     return super().save(*args, **kwargs)


# class Image(Model):
#     id = IntegerField(primary_key=True)
#     user = ForeignKeyField(Event, backref="messages", on_delete="CASCADE")  # 参照先が削除された場合は削除する
#     content = TextField()
#     pub_date = TimestampField(default=datetime.datetime.now)

#     class Meta:
#         database = db
#         table_name = "images"


# データベースの初期化
db.create_tables([Event, User])
db.pragma("foreign_keys", 1, permanent=True)  # on_deleteを動作させるオプション設定
