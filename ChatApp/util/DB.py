import pymysql

class DB:
    def getConnection():
        try:
            conn = pymysql.connect(
            host="db",
            db="chatapp",
            user="testuser",
            password="testuser",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
            return conn
        except pymysql.MySQLError as e:
            print(f"コネクションエラーです: {e}")
            return None
