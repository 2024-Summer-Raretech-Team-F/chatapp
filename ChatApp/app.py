from flask import Flask, request, redirect, render_template, session, flash, abort, url_for
from datetime import timedelta
import calendar
from datetime import datetime


import hashlib
import uuid
import re

from models import dbConnect

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


@app.route('/home',methods=['GET','POST'])
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

    # SQLからユーザー取得
    users_data = dbConnect.getUser('satoru@example.com')

    print(users_data)


    return render_template('registration/home.html',year=year,month=month,month_days=month_days,today=today,child_class=child_class,teacher=teacher,teacher_message=teacher_message,teacher_message_time=teacher_message_time,student_name=student_name,group_name=group_name,group_message=group_message,group_message_time=group_message_time,users_data=users_data)



#お知らせ一覧(全て)を表示させる
@app.route('/notices', methods=['GET'])
def get_all_notices():
    notices = dbConnect.getAllNotices()
    return notices


#学年でお知らせを絞る
@app.route('/notices/grade/<category>', methods=['GET'])
def get_notice_by_grade(category):
    notices = dbConnect.getNoticeByGrade(category)
    return notices


#お知らせの作成
@app.route('/notices/add_notice', methods=['POST'])
def add_notice():
    title = request.form.get('title')
    description = request.form.get('description')
    post_data = request.form.get('post_data')
    user_id = request.form.get('user_id')
    
    user = dbConnect.getUserById(user_id)
    
    if user is None or user['role'] != 'teacher':
        abort(403)
        
    dbConnect.createNotice(title, description, post_data, user_id)
    
    flash("お知らせが作成されました！")  
    return redirect(url_for('get_all_notices')) 


# お知らせの更新(編集)
@app.route('/notices/<int:notice_id>', methods=['PUT'])
def edit_notice(notice_id):
    title = request.form.get('title')
    description = request.form.get('description')
    post_data = request.form.get('post_data')
    user_id = request.form.get('user_id')
    
    user = dbConnect.getUserById(user_id)
    
    if user is None or user['role'] != 'teacher':
        abort(403)
    
    dbConnect.updateNotice(notice_id, title, description, post_data)
    
    flash("お知らせが更新されました")
    return redirect(url_for('get_all_notices'))


#お知らせの削除
@app.route('/notices/<int:notice_id>', methods=['DELETE'])
def delete_notice(notice_id):
    user_id = request.form.get('user_id')
    
    user = dbConnect.getUserById(user_id)
    
    if user is None or user['role'] != 'teacher':
        abort(403)
        
    dbConnect.deleteNotice(notice_id)
    
    flash("お知らせが削除されました。")
    return redirect(url_for('get_all_notice'))




if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
