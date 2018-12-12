from flask import render_template, request, redirect, url_for
from . import app
from .util import fetch_records, select_record, insert_record, update_record, delete_record, flash_message, check_action, is_form_filled
from .auth import login_required, get_user_id

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    rs = fetch_records(get_user_id())
    if not rs:
        flash_message([('No record found.', 'warning')])
    return render_template('list.html', title='Top Page', mode='home', rs=rs)

@app.route('/add/', methods=['GET'])
@app.route('/update/<int:id>/', methods=['GET'])
@app.route('/delete/<int:id>/', methods=['GET'])
@login_required
def crud_get(id=None):
    if id is None:
        #When requested URL is to add a record.
        return render_template('crud.html', title='Your Entry')
    
    #When requested URL is either to update or delete a record.
    r = select_record(id, get_user_id())
    action = check_action(request.url_rule)
    if not r or action is None:
        #If no such record exists or invalid actions.
        flash_message([('Bad Request.', 'error'), ('Back Home and Start Over.', 'warning')])
        return render_template('list.html', title='Bad Request')
    else:
        #When everything is OK with the request, show the confirmation page.
        date = str(r[2])
        date = date[0:4] + '-' + date[4:6] + '-' + date[6:]
        return render_template('crud.html', title='Your Entry', date=date, what=r[3], cal=r[4], rate=r[5], meal=r[6], action=action)

@app.route('/add/', methods=['POST'])
@app.route('/update/<int:id>/', methods=['POST'])
@app.route('/delete/<int:id>/', methods=['POST'])
@login_required
def crud_post(id=None):
    action = check_action(request.url_rule)
    mode = request.form.get('mode')
    date = request.form.get('date')
    what = request.form.get('what')
    cal = request.form.get('cal')
    rate = request.form.get('rate')
    meal = request.form.get('meal')
    if not is_form_filled(date, what, cal, rate, meal):
        flash_message([('Please check your entry.', 'error')])
        return render_template('crud.html', title='Your Entry', date=date, what=what, cal=cal, rate=rate, meal=meal, action=action)
    if mode == 'confirm':
        if action == 'add':
            insert_record(get_user_id(), date, what, cal, rate, meal)
        elif action == 'update':
            update_record(id, get_user_id(), date, what, cal, rate, meal)
        elif action == 'delete':
            delete_record(id, get_user_id())
        return redirect(url_for('home'))

    #If the request is other than 'confirm' => 'cancel' upon the confirmation page.
    return render_template('crud.html', title='Confirm Entry', date=date, what=what, cal=cal, rate=rate, meal=meal, mode=mode)
