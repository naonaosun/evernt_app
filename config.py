from datetime import datetime
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
#         migrator.add_column('events', 'lat', CharField(null=True)),
#         migrator.add_column('events', 'lng', CharField(null=True))
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
    lat = CharField(null=True)
    lng = CharField(null=True)
    url = CharField(null=True)
    image = CharField(null=True)  # 画像ファイル名を保存するフィールド

    def get_start_date(self):  # 日付を変換するメソッドを追加
        if self.start_date:
            if isinstance(self.start_date, str):
                # 文字列からdatetimeに変換
                self.start_date = datetime.fromisoformat(self.start_date)
            return self.start_date.strftime("%Y/%m/%d")
        return "未設定"

    def get_end_date(self):  # 日付を変換するメソッドを追加
        if self.end_date:
            if isinstance(self.end_date, str):
                # 文字列からdatetimeに変換

                self.end_date = datetime.fromisoformat(self.end_date)
            return self.end_date.strftime("%Y/%m/%d")
        return "未設定"

    class Meta:
        database = db
        table_name = "events"



class EventImage(Model):
    user = ForeignKeyField(User, backref="images", on_delete="CASCADE")
    event = ForeignKeyField(Event, backref="images", on_delete="CASCADE")
    posted_date = DateTimeField(default=datetime.now)
    image_path = CharField()  # 画像ファイルのパスを保存するフィールド

    class Meta:
        database = db
        table_name = "event_images"


# ★detaフィールドの削除★1～5を順を追って実行
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
db.create_tables([Event, User, EventImage])
db.pragma("foreign_keys", 1, permanent=True)  # on_deleteを動作させるオプション設定
