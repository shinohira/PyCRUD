from flask import Flask, session, g
import pg8000, os

__version__ = '0.0.1'
__all__ = ["", ""]

app = Flask(__name__)
app.config.from_object('config.DevConfig')

@app.before_request
def before_request():
    #Create DB connection with row_factory Row, so tht result can be accessed by column name.
    #g.db = sqlite3.connect(os.path.join(app.instance_path, 'app.db'))
    #g.db.row_factory = sqlite3.Row
    g.db = pg8000.connect(
        host=app.config['HOST'],
        database=app.config['DATABASE'],
        user=app.config['USER'],
        password=app.config['PASSWORD']
    )

    #Retrieve user ID from cookie session and restore in g object.
    user_id = session.get('user_id')
    if user_id is None:
        g.user_id = None
    else:
        c = g.db.cursor()
        c.execute("select * from users where user_id = %s", (user_id,))
        r = c.fetchone()
        g.user_id = r[0]

@app.after_request
def after_request(response):
    if g.db is not None:
        g.db.close()
    return response

import PyEt.views
import PyEt.auth