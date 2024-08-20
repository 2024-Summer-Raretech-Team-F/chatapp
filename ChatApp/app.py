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

@app.route('/')
def jump():
    return redirect('login')


# サインアップページの表示
@app.route('/signup')
def signup():
    return render_template('registration/signup.parent.html')


#サインアップ処理
@app.route('/signup', methods=['POST'])
def userSignup():
    name_kanji_full = request.form.get('name_kanji_full')
    name_kana_full = request.form.get('name_kana_full')
    grade = request.form.get('grade')
    section = request.form.get('section')
    parent_name = request.form.get('parent_name')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if name_kanji_full == '' or name_kana_full == '' or grade == '' or section == '' or parent_name == ''or phone_number == '' or email =='' or password1 == '' or password2 == '':
        flash('空のフォームがあるようです')
    elif password1 != password2:
        flash('二つのパスワードの値が違っています')
    elif re.match(pattern, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        user_id = uuid.uuid4()
        password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
        DBuser = dbConnect.getUser(email)

        if DBuser != None:
            flash('既に登録されているようです')
        else:
            dbConnect.createUser(user_id, name_kanji_full, name_kana_full, email, password)
            UserId = str(user_id)
            session['user_id'] = UserId
            return redirect('/login')
    return redirect(url_for('auth'))


# ログインページの表示
@app.route('/login')
def login():
    return render_template('registration/login.html')

# ログイン処理
@app.route('/login', methods=['GET', 'POST'] )
def userLogin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        auth_key_input = request.form.get('auth_key')
        
        user = dbConnect.getUser(email)
        
        if user and hashlib.sha256(user[password], password):
            school_id = user['school_id']
            auth_key = dbConnect.getAuthKey(school_id)
                    
            if auth_key_input == auth_key['teacher_auth_key']:
                role = 'teacher'
            elif auth_key_input == auth_key['parent_auth_key']:
                role = 'student'
            else:
                flash('Invalid authentication key')
                return redirect(url_for('login'))
            
            dbConnect.userRole(user['user_id'], role)
            
            flash("ログイン完了です！")
            return redirect(url_for('home'))
        else:
            flash("メールアドレスかパスワードが正しくありません")
            return redirect(url_for('login'))
    
    return  render_template('login.html')   


# 新規登録 / 学校IDの入力画面の表示
@app.route('/auth_signup')
def auth():
    return render_template('registration/auth-login.html')


@app.route('/auth_signup', methods=['POST'])
def getSchoolId():
    school_code = request.form.get('school_code')
    
    if not school_code:
        flash('学校IDを入力してください')
        return redirect(url_for('auth'))

    school_id = dbConnect.getSchoolCode(school_code)

    if school_id is None:
        flash('無効な学校IDです。正しい学校IDを入力してください。')
        return redirect(url_for('auth'))

    return redirect(url_for('home', school_id=school_code))



#トップページ
@app.route('/home',methods=['GET','POST'])
def home():

    school_id = session.get('school_id')
    email = session.get('email')

    # 現在の年月日を取得
    now = datetime.now()
    year = now.year
    month = now.month
    today = now.day

    #カレンダー作成
    
    # 週の始まりを日曜にする
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year,month)

    # チャットデータ
    # user_data = dbConnect.getUser(email)
    # grade = user_data['grade']
    # section = user_data['section']
    
    # child_class = dbConnect.getAcademicLevel(grade, section)
    # teacher_name = user_data['name_kanji_full']
    child_class = "5年3組"
    teacher = "佐藤　道哉"
    teacher_message = "本日もよろしくお願いします"
    teacher_message_time = "7:46"
    student_name = "田中　智樹"
    group_name = "グループ"
    group_message = "グループメッセージだよ〜"
    group_message_time ="7:50 "
    

    return render_template('index.html', year=year, month=month, month_days=month_days, today=today, child_class=child_class, teacher=teacher, teacher_message=teacher_message, teacher_message_time=teacher_message_time, student_name=student_name, group_name=group_name, group_message=group_message, group_message_time=group_message_time)



#お知らせ一覧(全て)を表示させる
@app.route('/notices', methods=['GET'])
def get_all_notices():
    main_notices = dbConnect.getAllNotices()
    return render_template('notice/notice_list.html', main_notices=main_notices)



@app.route('/notice/<notice_id>', methods=['GET'])
def get_notice_by_id(notice_id):
    notices = dbConnect.getNoticeById(notice_id)
    return render_template('notice/notice_main.html' , notices=notices)


#学年でお知らせを絞る
@app.route('/notices/grade/<category>', methods=['GET'])
def get_notice_by_grade(category):
    grade = dbConnect.getNoticeByGrade(category)
    return render_template('notice/notice_list.html', grade=grade)


#お知らせ作成ページの表示
@app.route('/notices/add_notice', methods=['GET'])
def create_notice():
    return render_template('notice/notice_create.html')


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
@app.route('/notices/<notice_id>', methods=['PUT'])
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
@app.route('/notices/<notice_id>', methods=['DELETE'])
def delete_notice(notice_id):
    user_id = request.form.get('user_id')

    user = dbConnect.getUserById(user_id)

    if user is None or user['role'] != 'teacher':
        abort(403)

    dbConnect.deleteNotice(notice_id)

    flash("お知らせが削除されました。")
    return redirect(url_for('get_all_notice'))

##チャットの処理
#チャットグループの表示
@app.route('/home')
def show_group():
    channels = dbConnect.getChannelAll()
    return render_template('home.html', channels=channels)


#チャットの表示
@app.route('/chat/<group_id>')
def detail(group_id):
    # user_id = session.get('user_id')
    # if user_id is None:
    #     return redirect('/login')
    
    channels = dbConnect.getChannelAll(group_id)
    message = dbConnect.getMessageAll(group_id)
    
    return render_template('chat_main.html', channels=channels, message=message)


#チャットの送信
@app.route('/message', methods=['POST'])
def add_message():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    message = request.form.get('message')
    group_id = request.form.get('group_id')

    if message:
        dbConnect.createMessage(user_id, group_id, message)

    return redirect('/chat/{group_id}'.format(group_id = group_id))


#チャットの削除
@app.route('/delete_message', methods=['POST'])
def delete_message():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    message_id = request.form.get('message_id')
    group_id = request.form.get('group_id')

    if message_id:
        dbConnect.deleteMessage(message_id)

    return redirect('/chat/{group_id}'.format(group_id=group_id))


#設定画面の表示
@app.route('/setting')
def userSetiing():
    user_id = session.get('user_id')
    user = dbConnect.getUser(user_id)
    return render_template('settings.html', user=user)


@app.route('/setting/edit', methods=['POST', 'GET'])
def editUserSetting():
    user_id = session.get('user_id')
    if request.method == 'POST':
        name_kanji_full = request.form['kidname-kanji_settings']
        name_kana_full = request.form['kidname-kana_settings']
        parent_name = request.form['parents-name_settings']
        phone_number = request.form['phone-number_settings']
        email = request.form['mail-settings']
        password = request.form['password_settings']
        
        dbConnect.updateUser(user_id, name_kanji_full, name_kana_full, parent_name, phone_number, email, password)
        
        return redirect(url_for('userSetting'))
    
    user = dbConnect.getUserById(user_id)
    return render_template('settings_edit.html', user=user)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'),404

@app.errorhandler(500)
def page_not_found(error):
    return render_template('error/500.html'),500



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
