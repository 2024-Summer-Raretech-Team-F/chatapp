from flask import Flask, abort, pymysql
from util.DB import DB

class dbConnect:
    def getSchoolCode(school_code, school_name, parent_auth_key, teacher_auth_key):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO schools (school_code, school_name, parent_auth_key, teacher_auth_key) VALUES (%s, %s, %s, %s);"
            cur.execute(sql, (school_code, school_name, parent_auth_key, teacher_auth_key))
            conn.commit()
        except Exception as e:
            print(f'{e} が発生しています')
            abort(500)
        finally:
            cur.close()


    def createUser(name_kanji_full, name_kana_full, parent_name, email, password, role, phone_number, academic_level_id, school_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO users (user_kanji_full, user_kana_full, parent_name, email, password, role, phone_number, academic_level_id, school_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cur.execute(sql, (name_kanji_full, name_kana_full, parent_name, email, password, role, phone_number, academic_level_id, school_id))
            conn.commit()
        except Exception as e:
            print(f'{e} が発生してます')
            abort(500)
        finally:
            cur.close()


    def getUser(email):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM users WHERE email=%s;"
            cur.execute(sql, (email))
            user = cur.fetchone()

            return user
        except Exception as e:
            print(f'{e} が発生しています')
            abort(500)
        finally:
            cur.close()


    def updateUser(user_id, name_knaji_full, name_kana_full, parent_name, phone_number,email, password):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "UPDATE users SET name_kanji_full = %s, name_kana_full = %s, parent_name = %s, phone_number = %s, email = %s, password = %s WHERE user_id = %s;"
            cur.execute(sql, (user_id, name_knaji_full, name_kana_full, parent_name, phone_number,email, password))
            conn.commit()
        except Exception as e:
            print(f'{e} が発生しています') 
            abort(500)
        finally:
            cur.close()       


    def getGroups():
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM groups;"
            cur.execute(sql)
            groups = cur.fetchall()
            return groups
        except Exception as e:
            print(f'{e} が発生しています')
            abort(500)
        finally:
            cur.close()


    def getMessageAll(group_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT message_id, u.user_id, user_name, message FROM messages AS m INNER JOIN users AS u ON m.user_id = u.user_id WHERE group_id = %s"
            cur.execute(sql,(group_id))
            messages = cur.fetchall()
            return messages
        except Exception as e:
            print(f'{e} が発生しています')
            abort(500)
        finally:
            cur.close()


##お知らせ一覧の処理

    def getAllNotices():
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT notice_id, title, description, post_data, created_at, teacher_id FROM notices;"
            cur.execute(sql)
            notices = cur.fetchall()
            return notices
        except Exception as e:
            print(f'{e} が発生しています')
            abort(500)
        finally:
            cur.close()


    def getNoticeById(notice_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT notice_id, title, description, post_data, created_at,teacher_id FROM notices WHERE noitced_id = %s;"
            cur.execute(sql, (notice_id))
            notice = cur.fetchone()
            return notice
        except Exception as e:
            print(f'{e} が発生しています')
            abort(500)
        finally:
            cur.close()


    def creatNotice(title, description, post_data, teacher_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO notices (title, description, post_data, teacher_id) VALUES (%s, %s, %s, %s)"
            cur.execute(sql, (title, description, post_data, teacher_id))
            conn.commit()
        except Exception as e:
            print(f'{e} が発生しています')
            abort(500)
        finally:
            cur.close()


    def updateNotice(notice_id, title, description, post_date):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "UPDATE notices SET title = %s, description = %s, post_date = %s WHERE notice_id = %s;"
            cur.execute(sql, (title, description, post_date, notice_id))
            conn.commit()
        except Exception as e:
            print(f'{e} が発生しています')
            abort(500)
        finally:
            cur.close()


    def deleteNotice(notice_id):
            try:
                conn = DB.getConnection()
                cur = conn.cursor()
                sql = "DELETE FROM notices WHERE notice_id = %s;"
                cur.execute(sql, (notice_id))
                conn.commit()
            except Exception as e:
                print(f'{e} が発生しています')
                abort(500)
            finally:
                cur.close()



    def getNoticeByGrade(category):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT notice_id, title, description, post_date, created_at, teacher_id, category FROM notices WHERE category = %s;"
            cur.execute(sql, (category))
            notices = cur.fetchall()
            return notices
        except Exception as e:
            print(f'{e} が発生しています')
            abort(500)
        finally:
            cur.close()


    def getNoticeByTitle(title):
        try:
            conn = DB.getConnection() 
            cur = conn.cursor()
            sql = "SELECT notice_id, title, description, post_date, created_at, teacher_id, category FROM notices WHERE title LIKE %s;"  
            search_title = f'%{title}%'
            cur.execute(sql, (search_title))
            notices = cur.fetchone()
            return notices
        except Exception as e:
            print(f'{e} が発生しています')
            abort(500)
        finally:
            cur.close()

