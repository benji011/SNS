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
DATA_FILE_USER = 'userlist.dat'
DATA_FILE_VIDEO = 'videodata.dat'

# アカウント登録:　情報をデータベースに保存します
@application.route('/register', methods=['POST'])
def register_account(): 
    server = MySQLdb.connect(host="localhost", db="socialnetwork", user="msusr", charset="utf8")
    cursor = server.cursor()

    name = request.form.get('username')
    email = request.form.get('email')
    country = request.form.get('country')
    # ユーザー名、メールアドレスとパスワードをデータベースに登録します
    
    updatelist = "insert into user_account (name, email, country) values ('%s', '%s', '%s')"
    cursor.execute(updatelist % (name, email, country))

    server.commit()
    cursor.close()
    server.close()

    return redirect('/')

def copy_user(name):
    database = shelve.open(DATA_FILE_USER)

    if 'user_list' not in database:
        user_list = []
    else:
        user_list = database['user_list']

        user_list.insert(0, {
            'name': name
        })
        database['user_list'] = user_list
        database.close()

def load_user():
    database = shelve.open(DATA_FILE_USER)
    user_list = database.get('user_list',[])
    database.close()
    return user_list    

# ログイン:　データベースに保存されている情報を確認して、真偽を行います
# アカウントログインのプログラミングが完成です。次はHTMLファイルにつなげます
@application.route('/logged_in', methods=['POST'])
def login():
    server = MySQLdb.connect(host="localhost", db="socialnetwork", user="msusr", charset="utf8")
    cursor = server.cursor()

    name = request.form.get('name')
    register_account()

    #クエリーで保存されている情報を取得しようとします
    search =  "select * from user_account where name=%s"
    cursor.execute(search, name)

    result = cursor.fetchall()

    for row in result:
       user_name = row[0].encode('utf-8')
       print "コピーユーザー"
       copy_user(user_name)
       print"ユーザー名をコピーします"
       
    if name not in search:
        print"no account found"

    cursor.close()
    server.close()
    return render_template('loggedin.html')

# ログインした後、ログアウトされないようにloggedin.htmlをルートとして扱います。
@application.route('/main')
def logged_in():

    comment_list = load_comment()
    user_list = load_user()
    video_list = load_video()
    return render_template('/loggedin.html', comment_list=comment_list, user_list=user_list, video_list=video_list)

# 動画を保存します
def save_video(post_video):
    video_database = shelve.open(DATA_FILE_VIDEO)

    if 'video_list' not in video_database:
        video_list=[]
    else:
        video_list = video_database['video_list']
        video_list.insert(0, {
            'post_video': post_video
        })
    video_database['video_list'] = video_list
    video_database.close()

# 動画データをリストから読み込みます
def load_video():
    video_database = shelve.open(DATA_FILE_VIDEO)
    video_list = video_database.get('video_list',[])
    video_database.close()

    return video_list

# 動画を投稿します
@application.route('/post_video', methods=['POST'])
def post_video():
    post_video = request.form.get('post_video')
    save_video(post_video)

    return redirect('/main')

# ユーザーのつぶやきをguestbookのように小型データベース・リストに保管して、ウェブページへ表示させる
def save_comment(comment):
    #つぶやきをdatファイルに保存します
    database = shelve.open(DATA_FILE)
   
    if 'comment_list' not in database:
        comment_list = []
    else:
        comment_list = database['comment_list']

    # つぶやきをデータベースに保存します
    comment_list.insert(0,{ 
        'comment': comment
        })

    database['comment_list'] = comment_list
    database.close()

    #データベースにcomment_listがなければ、新しくリストを作ります
    """投稿データリスト、後にする
    """

# ユーザーのつぶやきを取得します
def load_comment():

    #保存された投稿を取得します
    database = shelve.open(DATA_FILE)
    # comment_listを返します。データがばければ空リストを返します
    comment_list = database.get('comment_list',[]) 
    database.close()
    return comment_list

@application.route('/')
def index():
    register_account()
    return render_template('index.html')

# ユーザーのつぶやき・コメントを投稿します。guestbookのようにみつの関数をわけて、当関数にまとめます。
# ユーザー名とメールアドレスを直接入力することなくMySQLデータベースに直接アクセスして情報を取\取得します
# データベースをアクセスしてユーザー名とメールアドレスをコピーします

@application.route('/post', methods=['POST'])
def tsubuyakeyou():
    # ユーザーはすでにログインされているため、名前とメール情報を受け取らなくてもいい
    # 必ず日付をつぶやきごとにつけます (後にする)
    
    comment = request.form.get('comment')

    save_comment(comment)
    return redirect('/main')

if __name__ == "__main__":
    print "これはテストです。register_account(名前、メール、パスワードを入力するとアカウントを登録することができます)"
    print ""

application.run('127.0.0.1', 5000, debug=True)
