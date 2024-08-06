from flask import Flask, abort , pymysql
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


    def createUser(user_kanji_full, user_kana_full, parent_name, email, password, role, phone_number, academic_level_id, school_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO users (user_kanji_full, user_kana_full, parent_name, email, password, role, phone_number, academic_level_id, school_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cur.execute(sql, (user_kanji_full, user_kana_full, parent_name, email, password, role, phone_number, academic_level_id, school_id))
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