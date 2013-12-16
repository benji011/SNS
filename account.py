# encoding: utf-8

# アカウント登録：　情報をデーターベースに保存する
# ログイン：　データベースに保存されている情報を確認して、真偽を行います
# つぶやき；つぶやきをデータベースに保存して表示してくれる機能
# サーバーへ接続関数を作ります。関数に入るたびに同じコードを常に書き直さなくてもいい

import MySQLdb


# サーバーへ接続関数:　関数に入るたびに同じコードを常に書き直さなくてもいい
def connect_to_server():
    server = MySQLdb.connect("localhost", db="socialnetwork", user="msusr", charset="utf8")
    cursor = server.cursor()
    server.commit()
    cursor.close()
    server.close()


# アカウント登録:　情報をデータベースに保存します
def register_account(name, email, country): 
    
    connect_to_server()

    # ユーザー名、メールアドレスとパスワードをデータベースに登録します
    sql = u"insert into user_account values('{}','{}','{}' )".format(name, email, country)
    cursor.execute(sql)
    server.commit()

    cursor.close()
    server.close()

    return "アカウント登録は成功です"



# ログイン:　データベースに保存されている情報を確認して、真偽を行います
def login(name, email, country):
    connect_to_server()
    return "ログインは成功です"


if __name__ == "__main__":


    print "これはテストです。register_account(名前、メール、パスワードを入力するとアカウントを登録することができます)"
    print ""
