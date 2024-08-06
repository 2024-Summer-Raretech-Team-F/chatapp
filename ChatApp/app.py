from flask import Flask, request, redirect, render_template, session, flash, abort
from datetime import timedelta
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

@app.route('/auth')
def auth():
    return render_template('registration/auth.html')

# @app.route('home')
# def home():
#     return


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
