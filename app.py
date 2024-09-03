from flask import Flask, render_template, request, redirect, url_for
from peewee import SqliteDatabase, Model, CharField, DateTimeField

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# SQLiteデータベースの設定
db = SqliteDatabase("events.db")


# データベースモデルの定義
class Event(Model):
    name = CharField()
    date = DateTimeField()
    place = CharField()
    address = CharField()
    url = CharField(null=True)

    class Meta:
        database = db


# データベースの初期化
db.connect()
db.create_tables([Event], safe=True)  # 'safe=True'で既に存在するテーブルを上書きしない



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # フォームから送信されたデータを取得
        name = request.form["name"]
        date = request.form["date"]
        place = request.form["place"]
        address = request.form["address"]
        url = request.form.get('url', '')

        # データベースに新しいイベントを保存
        Event.create(name=name, date=date, place=place, address=address, url=url)

        return redirect(url_for("index"))

    # データベースからすべてのイベントを取得
    events = Event.select()
    return render_template("index.html", events=events)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
