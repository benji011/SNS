#coding: utf-8
# アカウント登録：　情報をデーターベースに保存する
# ログイン：　データベースに保存されている情報を確認して、真偽を行います
# つぶやき；つぶやきをデータベースに保存して表示してくれる機能

import MySQLdb

def register_account(name, email, country):

  registeredStatus = false
  # ユーザー名、メールアドレスとパスワードをデータベースに登録します
  
  # 登録が成功したメッセージを表示します
  if (registeredStatus == True):
    print "アカウント登録が成功しました"
  else:
      print "登録が失敗しました"

  

# call register_account first when file is executed
# データーベースを起動させる
if __name__ == "__main__":
      connector = MySQLdb.connect(host="localhost", db="socialnetwork", user="msusr", password="mspsw", charset="utf8")
  cursor = connector.cursor()
  cursor.execute("select * from user_account")

  print "これはテストです。register_account(名前、メール、パスワードを入力するとアカウントを登録することができます)"
  print ""
