import sqlite3
import os
from flask import g
from rmcontest import app


### Database basics
###################

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.cli.command('initdb')
def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    print('Initialized the database.')


def authenticate_user(username,hashed_pass):
    db = get_db()
    cur = db.execute('select * from users WHERE username = ? AND password = ?',[username,hashed_pass])
    users = cur.fetchall()
    if len(users):
        return users[0]['user_id']
    else:
        return False


### Getting problem information
###############################


def get_completed_problems(user_id):
    db = get_db()
    cur = db.execute('select * from ')




