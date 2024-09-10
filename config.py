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
from playhouse.migrate import SqliteMigrator, migrate


# SQLiteデータベースの設定
db = SqliteDatabase("db.sqlite")
db.connect()  # データベースに接続

# マイグレーターの設定
migrator = SqliteMigrator(db)

# トランザクションを開始してマイグレーションを実行
with db.atomic():
    migrate(
        migrator.add_column('events', 'content', TextField(null=True))  # 追加するフィールドを記載
    )


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


