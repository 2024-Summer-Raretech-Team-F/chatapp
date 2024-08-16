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

# ログイン処理
@app.route('/login', methods=['POST'] )
def userLogin():
    email = request.form.get('email')
    password = request.form.get('password')
        
    if email == '' or password == '':
        flash('入力されていないフォームがあります')
    else:
        user = dbConnect.getUser(email)
        if user is None:
            flash('このユーザーは存在しません')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user['password']:
                flash('パスワードが間違っています')
            else:
                session['user_id'] = user['user_id']
                return redirect('/home')    
    return redirect('/login')                

# 新規登録 / 学校IDの入力画面の表示
@app.route('/auth')
def auth():
    return render_template('registration/auth.html')


@app.route('/auth', methods=['POST'])
def getSchoolId():
    school_code = request.form.get('school_code')  
    
    if not school_code:
        flash('学校IDを入力してください')
        return redirect(url_for('auth'))  
    
    school_id = dbConnect.getSchoolCode(school_code)
    
    if school_id is None:
        flash('無効な学校IDです。正しい学校IDを入力してください。')
        return redirect(url_for('auth'))
    
    return redirect(url_for('home', school_id=school_id))




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


#チャットグループの表示
@app.route('/home')
def show_group():
    groups = dbConnect.getGroups()
    render_template('chat_main.html', groups=groups)
    

#チャット欄の表示
@app.route('/chat/<group_id>')
def detail(group_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/loign')
    
    group_id = group_id
    group = dbConnect.getGroups(group_id)
    message = dbConnect.getMessageAll(group_id)
    
    return render_template('home.html', group=group, message=message)


#チャットの送信
@app.route('/message', methods=['POST'])
def add_message():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    
    message = request.form.get('message')
    group_id = request.get('group_id')
    
    if message:
        dbConnect.createMessage(user_id, group_id, message)
        
    return redirect('/chat/{group_id}'.format(group_id = group_id))    




if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
