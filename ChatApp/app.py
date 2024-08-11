from flask import Flask, request, redirect, render_template, session, flash, abort
from datetime import timedelta
import calendar
from datetime import datetime
import hashlib
import uuid
import re

# from models import dbConnect

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)


# ログインページの表示
@app.route('/login')
def login():
    return render_template('registration/login.html')

@app.route('/auth',methods=['GET','POST'])
def auth():
    return render_template('registration/auth.html')


@app.route('/home')
def home():
    # 現在の年月日を取得
    now = datetime.now()
    year = now.year
    month = now.month
    today = now.day

    #カレンダー作成
    #
    # 週の始まりを日曜にする
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year,month)

    # チャットデータ
    child_class = "5年3組"
    teacher = "佐藤　道哉"
    teacher_message = "本日もよろしくお願いします"
    teacher_message_time = "7:46"
    student_name = "田中　智樹"
    group_name = "グループ"
    group_message = "グループメッセージだよ〜"
    group_message_time ="7:50 "



    return render_template('registration/home.html',year=year,month=month,month_days=month_days,today=today,child_class=child_class,teacher=teacher,teacher_message=teacher_message,teacher_message_time=teacher_message_time,student_name=student_name,group_name=group_name,group_message=group_message,group_message_time=group_message_time)




if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
