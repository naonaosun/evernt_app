from flask import Flask, flash, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from peewee import SqliteDatabase, Model, CharField, DateTimeField
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import Event, User, EventImage
import os
from datetime import datetime
from func import user  # user.pyからBlueprintをインポート


# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"  # staticフォルダ内に画像を保存
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
    flash("ログインすると投稿ができます。")
    return redirect(
        url_for("user_bp.login")
    )  # ★blueprint名を指定(loginのルートをblueprintで定義しているため)


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
        content = request.form["content"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        place = request.form["place"]
        address = request.form["address"]
        url = request.form.get("url", "")
        # ファイルのアップロード処理
        if "image" in request.files:
            file = request.files["image"]
            if file and allowed_file(file.filename):
                # ファイル名の安全性を確保
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                # スラッシュ形式に変換
                file_path = file_path.replace("\\", "/")
                # 画像ファイルを指定のディレクトリに保存
                file.save(file_path)

                # 各データベースにイベントを保存
                event = Event.create(
                    name=name,
                    content=content,
                    start_date=start_date,
                    end_date=end_date,
                    place=place,
                    address=address,
                    url=url,
                )

                EventImage.create(
                    event=event,
                    user=current_user,  # ログイン中のユーザーを取得
                    image_path=file_path,
                    posted_deat=datetime.now(),
                )

                flash("イベントの登録が完了しました！")  # 登録完了メッセージをflash
                return redirect(url_for("index"))
            else:
                flash("画像のアップロードに失敗しました。対応する形式のファイルを選択してください。")
                return redirect(request.url)

    return render_template("create_events.html")


# アップロードされた画像を保存するディレクトリ
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 許可するファイルの拡張子
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


# ファイル拡張子をチェックする関数
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# イベント詳細ページのルート
@app.route("/event/<int:event_id>", methods=["GET", "POST"])
def event_detail(event_id):
    # イベントIDに基づいてイベントを取得
    event = Event.get(Event.id == event_id)
    images = EventImage.select().where(EventImage.event == event)
    return render_template("event_detail.html", event=event, images=images)


# イベント画像の新規投稿ルート
@app.route("/event/<int:event_id>/postimage", methods=["GET", "POST"])
@login_required
def post_image(event_id):
    # イベントIDに基づいてイベントを取得
    event = Event.get(Event.id == event_id)
    images = EventImage.select().where(EventImage.event == event)

    if request.method == "POST":
        # ファイルのアップロード処理
        if "image" in request.files:
            file = request.files["image"]
            if file and allowed_file(file.filename):
                # ファイル名の安全性を確保
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                # スラッシュ形式に変換
                file_path = file_path.replace("\\", "/")
                # 画像ファイルを指定のディレクトリに保存
                file.save(file_path)

                # データベースにイベントを保存
                EventImage.create(
                    event=event,
                    user=current_user,  
                    image_path=file_path,
                    posted_date=datetime.now(),
                )

                flash("画像の登録が完了しました！")  # 登録完了メッセージをflash
                # リダイレクト先に event_id を渡す
                return redirect(url_for("event_detail", event_id=event_id))
            else:
                flash("画像のアップロードに失敗しました。対応する形式のファイルを選択してください。")

    return render_template("post_image.html", event=event, images=images)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
