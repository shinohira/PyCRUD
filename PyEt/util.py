from flask import g, flash
from werkzeug.security import check_password_hash
import pg8000

def fetch_records(user_id):
    c = g.db.cursor()
    c.execute("select * from pyet where user_id = %s order by date, id", (user_id,))
    return c.fetchall()

def select_record(id, user_id):
    c = g.db.cursor()
    c.execute("select * from pyet where id = %s and user_id = %s", (id, user_id))
    return c.fetchone()

def insert_record(user_id, date, what, cal, rate, meal):
    c = g.db.cursor()
    date = int(date.replace('-', ''))
    cal = int(cal)
    rate = int(rate)
    c.execute("insert into pyet (user_id, date, item, cal, rate, meal) values (%s, %s, %s, %s, %s, %s)", (user_id, date, what, cal, rate, meal))
    g.db.commit()

def update_record(id, user_id, date, what, cal, rate, meal):
    c = g.db.cursor()
    date = int(date.replace('-', ''))
    cal = int(cal)
    rate = int(rate)
    c.execute("update pyet set date = %s, item = %s, cal = %s, rate = %s, meal = %s where id = %s and user_id = %s", (date, what, cal, rate, meal, id, user_id))
    g.db.commit()

def delete_record(id, user_id):
    c = g.db.cursor()
    c.execute("delete from pyet where id = %s and user_id = %s", (id, user_id))
    g.db.commit()

def does_user_exist(user):
    c = g.db.cursor()
    c.execute("select * from users where user_id = %s", (user,))
    r = c.fetchone()
    if r:
        return True
    return False

def is_password_correct(user, password):
    c = g.db.cursor()
    c.execute("select * from users where user_id = %s", (user,))
    r = c.fetchone()
    if r and check_password_hash(r[1], password):
        return True
    return False

def check_action(url_rule):
    action = str(url_rule)
    if action.count('/delete'):
        return 'delete'
    elif action.count('/update'):
        return 'update'
    elif action.count('/add'):
        return 'add'
    return None

def is_form_filled(date, what, cal, rate, meal):
    if date and what and cal and rate:
        if date >= "2000-01-01" and date <= "2050-12-31":
            if len(what) <= 128:
                if int(cal) >= 0 and int(cal) <= 10000:
                    if int(rate) >= 0 and int(rate) <= 100:
                        if meal in ['Breakfast', 'Lunch', 'Supper']:
                            return True
    return False

def flash_message(alert_list):
    for msg, level in alert_list:
        flash(msg, category='label label-rounded label-'+level)
