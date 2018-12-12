from flask import redirect, render_template, url_for, request, session, g
from functools import wraps
from . import app
from .util import does_user_exist, is_password_correct, flash_message

@app.route('/login/', methods=['GET'])
def login_get():
    return render_template('login.html', title='Log in')

@app.route('/login/', methods=['POST'])
def login_post():
    user = request.form.get('user')
    password = request.form.get('password')
    if does_user_exist(user) and is_password_correct(user, password):
        #When credentials are OK, set user ID in persistent session so it's copied into g per each request.
        session.clear()
        session['user_id'] = user
        return redirect(url_for('home'))
    flash_message([('Looks like user ID or password is incorrect.', 'error')])
    return render_template('login.html', title='Log in', user=user)

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login_get'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user_id is None:
            flash_message([('You need to log in first.', 'warning')])
            return redirect(url_for('login_get'))
        return f(*args, **kwargs)
    return decorated_function

def get_user_id():
    return g.user_id

def set_user_id(user_id):
    g.user_id = user_id