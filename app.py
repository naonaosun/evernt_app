from flask import Flask, flash, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from peewee import SqliteDatabase, Model, CharField, DateTimeField
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import Event, User
import os
from func import user  # user.pyからBlueprintをインポート


# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)
app.secret_key = "secret"

# Flask-Loginの初期化
login_manager = LoginManager()
login_manager.init_app(app)

# Flask-Loginがユーザー情報を取得するためのメソッド
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

# ログインしていないとアクセスできないページにアクセスがあった場合の処理
@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for("user_bp.login"))   # ★blueprint名を指定(loginのルートをblueprintで定義しているため)

# user.pyに分割したBlueprintの登録
app.register_blueprint(user.app, url_prefix="/user")


# イベント一覧ページのルート
@app.route("/", methods=["GET", "POST"])
def index():  # データベースからすべてのイベントを取得
    events = Event.select()
    return render_template("index.html", events=events)


# イベント登録ページのルート
@app.route("/events", methods=["GET", "POST"])
@login_required
def create_events():
    if request.method == "POST":  # フォームから送信されたデータを取得
        name = request.form["name"]
        date = request.form["date"]
        place = request.form["place"]
        address = request.form["address"]
        url = request.form.get("url", "")

        # データベースに新しいイベントを保存
        Event.create(name=name, date=date, place=place, address=address, url=url)
        flash("イベントの登録が完了しました！")  # 登録完了メッセージをflash
        return redirect(url_for("index"))

    return render_template("create_events.html")


# イベント詳細ページのルート
@app.route("/event/<int:event_id>")
def event_detail(event_id):
    # イベントIDに基づいてイベントを取得
    event = Event.get(Event.id == event_id)
    return render_template("event_detail.html", event=event)


# 詳細ページに画像をアップロードする
# アップロードされた画像を保存するディレクトリ
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 許可するファイルの拡張子
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


# ファイル拡張子をチェックする関数
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload_image/<int:event_id>", methods=["POST"])
def upload_image(event_id):
    # ファイルがリクエストに含まれているかを確認
    if "image" not in request.files:
        return redirect(request.url)

    file = request.files["image"]

    # ファイルが選択されていない場合の処理
    if file.filename == "":
        return redirect(request.url)

    # ファイルが許可されたタイプであるかをチェック
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # データベースのイベントレコードを更新して画像名を保存
        event = Event.get(Event.id == event_id)
        event.image = filename
        event.save()

        return redirect(url_for("event_detail", event_id=event_id))

    return redirect(request.url)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
