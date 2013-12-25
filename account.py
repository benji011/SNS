# encoding: utf-8

# アカウント登録：　情報をデーターベースに保存する
# ログイン：　データベースに保存されている情報を確認して、真偽を行います
# つぶやき；つぶやきをデータベースに保存して表示してくれる機能
# 動画のシェアデータが消えないように小型データベース・リストを採用する必要があるのかもしれない

import MySQLdb
import shelve
from flask import Flask, request, render_template, redirect, escape, Markup

application = Flask(__name__)

DATA_FILE = 'tsubuyaki.dat'

# アカウント登録:　情報をデータベースに保存します
def register_account(name, email, country): 
    server = MySQLdb.connect(host="localhost", db="socialnetwork", user="msusr", charset="utf8")
    cursor = server.cursor()
    
    # ユーザー名、メールアドレスとパスワードをデータベースに登録します
    sql = u"insert into user_account values('{}','{}','{}')".format(name, email, country)
    cursor.execute(sql)
    server.commit()

    cursor.close()
    server.close()

    return "account has been registered アカウント登録は成功です"



# ログイン:　データベースに保存されている情報を確認して、真偽を行います
# アカウントログインのプログラミングが完成です。次はHTMLファイルにつなげます
# Help: TypeError: execute() takes at most 3 arguments (4 given)のエラーメッセージが出てきているがなぜ？？
# 問題は47行目に示されていますが、４番目の引数はどこで定義されているかわかりません
@application.route('/logged_in', methods=['POST'])
def login():
    server = MySQLdb.connect(host="localhost", db="socialnetwork", user="msusr", charset="utf8")
    cursor = server.cursor()

    name = request.form.get('name')
    email = request.form.get('email')

    #クエリーで保存されている情報を取得しようとします
    search =  "select * from user_account where name=%s and email=%s"
    cursor.execute(search, name, email)

    result = cursor.fetchall()

    for row in result:
        print"name-- " +row[0].encode('utf-8')
        print"email--" +row[1].encode('utf-8')
    if row in result is None:
        print "no account registered"
    cursor.close()
    server.close()
    return redirect('/logged_in')

# YouTubeの動画を表示してくれる機能
# 埋め込みコードを返してもらって、ウェブページを後に任せる
def post_video(linked_video):
    embedded_code = ""
    video_list = []
    video_list_append(linked_video)

    return embedded_code

# ユーザーのつぶやきをguestbookのように小型データベース・リストに保管して、ウェブページへ表示させる
def save_comment(name, comment, create_at):
    #shelveモジュールでデータベースファイルを開きます
    database = shelve.open(DATA_FILE)
    
    #データベースにcomment_listがなければ、新しくリストを作ります
    """投稿データリスト、後にする
    """
    

    #リストの先端に投稿データを追加します
    #comment_list = database.get('comment_list',[])

# ユーザーのつぶやきを取得します
def load_comment():
    """投稿されたデータを返します。後にする
    """
    #shelveモジュールでデータベースファイルを開きます
    # database = shelve.open(DATA_FILE)

    # comment_listを返します。データがばければ空リストを返します
    

@application.route('/')
def index():
    return render_template('index.html')

# ユーザーのつぶやき・コメントを投稿します。guestbookのようにみつの関数をわけて、当関数にまとめます。
# ユーザー名とメールアドレスを直接入力することなくMySQLデータベースに直接アクセスして情報を取\取得します
# データベースをアクセスしてユーザー名とメールアドレスをコピーします
@application.route('/post', methods=['POST'])
def tsubuyakeyou():
    # ログインの真偽にテストをする
    return redirect('/')

if __name__ == "__main__":
    print "これはテストです。register_account(名前、メール、パスワードを入力するとアカウントを登録することができます)"
    print ""

application.run('127.0.0.1', 5000, debug=True)
