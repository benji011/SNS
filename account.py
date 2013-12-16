# encoding: utf-8

# アカウント登録：　情報をデーターベースに保存する
# ログイン：　データベースに保存されている情報を確認して、真偽を行います
# つぶやき；つぶやきをデータベースに保存して表示してくれる機能

import MySQLdb


# アカウント登録:　情報をデータベースに保存します
def register_account(name, email, country): 
    server = MySQLdb.connect(host="localhost", db="socialnetwork", user="msusr", charset="utf8")
    cursor = server.cursor()
    
    # ユーザー名、メールアドレスとパスワードをデータベースに登録します
    sql = u"insert into user_account values('{}','{}','{}' )".format(name, email, country)
    cursor.execute(sql)
    server.commit()

    cursor.close()
    server.close()

    return "account has been registered アカウント登録は成功です"



# ログイン:　データベースに保存されている情報を確認して、真偽を行います
def login(name):
    server = MySQLdb.connect(host="localhost", db="socialnetwork", user="msusr", charset="utf8")
    cursor = server.cursor()

    #Help: クエリーで保存されている情報を取得しようとします
    search =  "select * from user_account where name=%s"
    printResult = cursor.execute(search, name)

    return printResult


if __name__ == "__main__":

    print "これはテストです。register_account(名前、メール、パスワードを入力するとアカウントを登録することができます)"
    print ""
