import datetime
from flask_login import UserMixin
from peewee import (
    SqliteDatabase,
    Model,
    IntegerField,
    CharField,
    TextField,
    TimestampField,
    ForeignKeyField,
    DateTimeField,
)


# SQLiteデータベースの設定
db = SqliteDatabase("db.sqlite")


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
    date = DateTimeField()
    place = CharField()
    address = CharField()
    url = CharField(null=True)
    image = CharField(null=True)  # 画像ファイル名を保存するフィールド

    class Meta:
        database = db
        table_name = "events"


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
