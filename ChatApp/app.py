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

    if not all([name_kanji_full, name_kana_full, grade, section, parent_name, phone_number, email, password1, password2]):
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
            return redirect(url_for('signup')) 
        else:
            dbConnect.creatUser1(name_kanji_full, name_kana_full, email, password, phone_number)
            
            session['user_id'] = user_id
            session['name_kanji_full'] = name_kanji_full
            session['name_kana_full'] = name_kana_full
            session['grade'] = grade
            session['section'] = section
            session['parent_name'] = parent_name
            session['phone_number'] = phone_number
            session['email'] = email
            
            
            flash('登録が完了しました')
    return redirect(url_for('finish'))


#登録完了ページの表示
@app.route('/finish')
def finish():
    return render_template('registration/finish.html')


# ログインページの表示
@app.route('/login')
def login():
    return render_template('registration/login.html')

# ログイン処理
@app.route('/login', methods=['GET', 'POST'] )
def userLogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        auth_key_input = request.form['auth_key']
        
        session['email'] = email
        session['password'] = password
        session['auth_key_input'] = auth_key_input
        
        user = dbConnect.getUser(email)
        
        if user and hashlib.sha256(password.encode('utf-8')).hexdigest() == user['password']:
            school_id = user['school_id']
            auth_key = dbConnect.getAuthKey(school_id)
            
            if auth_key_input == auth_key['teacher_auth_key']:
                role = 'teacher'
            elif auth_key_input == auth_key['parent_auth_key']:
                role = 'student'
            else:
                flash('この認証キーは使用できません')
                return redirect(url_for('login'))
            
            dbConnect.userRole(user['user_id'], role)
            
            session['user_id'] = user['user_id']
            session['role'] = role
            session['school_id'] = school_id
            
            flash("ログイン完了です！")
            return redirect(url_for('home'))
        else:
            flash("メールアドレスかパスワードが正しくありません")
            return redirect(url_for('login'))
    
    return  render_template('login.html')   


# 新規登録 / 学校IDの入力画面の表示
@app.route('/auth_signup')
def auth():
    return render_template('registration/auth-signup.html')


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
    
    session['school_id'] = school_id
    
    return redirect(url_for('userSignup'))



@app.route('/auth_login')
def auth_login():
    return render_template('registration/auth-login.html')


@app.route('/auth_login', methods=['POST'])
def loginSchoolId():
    school_code = request.form.get('school_code')
    if not school_code:
        flash('学校IDを入力してください')
        return redirect(url_for('auth_login'))

    school_id = dbConnect.getSchoolCode(school_code)
    
    if school_id is None:
        flash('無効な学校IDです。正しい学校IDを入力してください。')
        return redirect(url_for('auth_login'))
    
    session['school_id'] = school_id
    
    return redirect(url_for('home'))


#トップページ
@app.route('/home',methods=['GET','POST'])
def home():
    school_id = session.get('school_id','None')
    user_id = session.get('user_id','None')
    
    if user_id is None or school_id is None:
        return redirect('/login')
    
    # 現在の年月日を取得
    now = datetime.now()
    year = now.year
    month = now.month
    today = now.day

    #カレンダー作成
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year,month)
    
    
    channels = dbConnect.getChannelAll()
    teacher = dbConnect.getUserById(user_id)
    
    #####################
    child_class = "5年3組"
    teacher = "佐藤　道哉"
    teacher_message = "本日もよろしくお願いします"
    teacher_message_time = "7:46"
    student_name = "田中　智樹"
    group_name = "グループ"
    group_message = "本日欠席します〜"
    group_message_time ="7:50 "
    

    return render_template('index.html', year=year, month=month, month_days=month_days, today=today, channels=channels,child_class=child_class, teacher=teacher, teacher_message=teacher_message, teacher_message_time=teacher_message_time, student_name=student_name, group_name=group_name, group_message=group_message, group_message_time=group_message_time)



#お知らせ一覧(全て)を表示させる
@app.route('/notices', methods=['GET'])
def get_all_notices():
    school_id = session.get('school_id','None')
    user_id = session.get('user_id','None')
    
    if user_id is None or school_id is None:
        return redirect('/login')
    
    allnotices = dbConnect.getAllNotices()
    return render_template('notice/notice_list.html', allnotices=allnotices)



@app.route('/notice/<notice_id>', methods=['GET'])
def get_notice_by_id(notice_id):
    school_id = session.get('school_id','None')
    user_id = session.get('user_id','None')
    
    if user_id is None or school_id is None:
        return redirect('/login')
    
    notices = dbConnect.getNoticeById(notice_id)
    return render_template('notice/notice_main.html' , notices=notices)


#学年でお知らせを絞る
@app.route('/notices/grade/<category>', methods=['GET'])
def get_notice_by_grade(category):
    grade = dbConnect.getNoticeByGrade(category)
    return render_template('notice/notice_list.html', grade=grade)


#タイトルで検索
@app.route('/notice/search ', methods=['GET'])
def get_notice_by_search(title):
    title = request.args.get('title')
    noticeTitle = dbConnect.getNoticeByTitle(title)
    return render_template('notice/notice_list.html', noticeTilte=noticeTitle)


#お知らせ作成ページの表示
@app.route('/notices/add_notice', methods=['GET'])
def create_notice():
    return render_template('notice/notice_create.html')


#お知らせの作成
@app.route('/notices/add_notice', methods=['POST'])
def add_notice():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    
    title = request.form.get('notice-title')
    description = request.form.get('maintext')
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
    return redirect(url_for('get_all_notices'))

##チャットの処理
#チャットグループの表示
@app.route('/home')
def show_channel():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    else:
        channels = dbConnect.getChannelAll()
    return render_template('home.html', channels=channels, user_id=user_id)


#チャットの表示
@app.route('/chat/<group_id>')
def detail(group_id):
    school_id = session.get('school_id','None')
    user_id = session.get('user_id','None')
    
    if user_id is None or school_id is None:
        return redirect('/login')
    
    group_id=group_id
    channels = dbConnect.getChannelById(group_id)
    messages = dbConnect.getMessageAll(group_id)
    
    return render_template('sample_chat.html', channels=channels, messages=messages, user_id=user_id, group_id=group_id)


#チャットの送信
@app.route('/message', methods=['POST'])
def add_message():
    school_id = session.get('school_id','None')
    user_id = session.get('user_id','None')
    
    if user_id is None or school_id is None:
        return redirect('/login')

    message = request.form.get('message')
    group_id = request.form.get('group_id')

    if message:
        dbConnect.createMessage(message, user_id, group_id)

    return redirect('/chat/{group_id}'.format(group_id = group_id))


#チャットの削除
@app.route('/delete_message', methods=['POST'])
def delete_message():
    school_id = session.get('school_id','None')
    user_id = session.get('user_id','None')
    
    if user_id is None or school_id is None:
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
    school_id = session.get('school_id','None')
    user_id = session.get('user_id','None')
    
    if user_id is None or school_id is None:
        return redirect('/login')
    
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
