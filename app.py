from flask import Flask, request, render_template, redirect, url_for
from peewee import SqliteDatabase, Model, CharField, DateTimeField
from datetime import datetime

# データベースの設定
db = SqliteDatabase("db.sqlite")

# モデルの定義
class Event(Model):
    title = CharField()
    date = DateTimeField()
    url = CharField(null=True)  # URL フィールドを追加

    class Meta:
        database = db
        table_name = "events"

# # データベーステーブルを作成
# db.connect()
# db.create_tables([Event])

# # Flask アプリケーションの設定
# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         title = request.form['title']
#         date = request.form['date']
#         url = request.form['url']

#         # 入力データをモデルに保存
#         Event.create(
#             title=title,
#             date=datetime.strptime(date, '%Y-%m-%d %H:%M:%S'),
#             url=url
#         )

#         return redirect(url_for('index'))

#     # 登録されたイベントを取得して表示
#     events = Event.select()
#     return render_template('index.html', events=events)

# if __name__ == '__main__':
#     app.run(debug=True)
