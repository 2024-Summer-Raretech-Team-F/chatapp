from flask import Flask, abort , pymysql
from util.DB import DB

class dbConnect:
    def getSchoolCode(school_code, school_name):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO schools (school_id, school_name) VALUES (%s, %s);"
            cur.execute(sql, (school_code, school_name))
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
        
    
    