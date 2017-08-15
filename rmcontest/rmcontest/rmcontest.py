from flask import Flask, request, redirect, url_for, abort, \
     render_template, Response, session, g
from flask_navigation import Navigation
from functools import wraps
from hashlib import sha1

import sqlite3
import time
import os
import sys

app = Flask(__name__) # create the application instance :)

app.config.from_object(__name__) # load config from this file , rmcontest.py
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'rmcontest.db'),
    SECRET_KEY='pQ3mFfla9x62jeva',
    USERNAME='admin',
    PASSWORD='default'
))



contest_started = False

	

##########################################################################
######################## AUTHENTICATION ##################################
##########################################################################

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            abort(401)

        return f(*args, **kwargs)
    return decorated
	
#------------------------------------------------------------------------#
##########################################################################



##########################################################################
######################## NAVIGATION BAR ##################################
##########################################################################

nav = Navigation(app)
nav.init_app(app)

nav.Bar('top', [
    nav.Item('Home', 'home_page'),
    nav.Item('Problems','problems_page'),
    nav.Item('Utilities', 'utilities_page')
])




#------------------------------------------------------------------------#
##########################################################################



##########################################################################
############################### LOGIN ####################################
##########################################################################

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pass = sha1(password.encode("ascii")).hexdigest()
        success = authenticate_user(username,hashed_pass)

        if success:
            session['logged_in'] = success
            return render_template('login.html',logged_in=True)
        else:
            return render_template('home.html',logged_in=False,error=True)


    else:
        print("")
    pass

@requires_login
@app.route('/logout',methods=['GET','POST'])
def logout():

    if request.method == 'POST':
        if 'logged_in' in session:
            del session['logged_in']
    return render_template('home.html',logged_in=False)

#------------------------------------------------------------------------#
##########################################################################


##########################################################################
############################### VIEWS ####################################
##########################################################################



@app.route('/')
@app.route('/home')
def home_page():
    logged_in = True
    if not session.get('logged_in'):
        logged_in = False
    return render_template('home.html',logged_in=logged_in)


@app.route('/utilities')
@requires_login
def utilities_page():
    return render_template('utilities.html')



## Problems
# 1) Galaxies
# 2) Shleeble number
# 3) zlnop propety search
# 4) sum of numbers 
# 5) traverse tree

## Ordered by difficulty -
# 4, 1, 5, 2, 3
# A, B, C, D, E

## Map problem letters to characters



@app.route('/problems')
@requires_login
def problems_page():
    user_id = session['logged_in']
    completed_problems = get_completed_problems(user_id)
    incomplete_problems = get_incomplete_problems(user_id)

    print("completed problems:",completed_problems)
    print("incomplete problems: ", incomplete_problems)
    return render_template(
        'problems.html',
        completed_problems=completed_problems,
        incomplete_problems=incomplete_problems
        )



@app.route('/problem<problem_num>')
@requires_login
def problem_page(problem_num,no_answer=False):
    return render_template(
        "problem" + str(problem_num) + '.html',
        no_answer=no_answer,
        input_file='/static/problems/input_' + str(problem_num) + '.txt',
        problem_num=problem_num
    )



    









#------------------------------------------------------------------------#
##########################################################################


##########################################################################
######################## PROBLEM LOGIC ###################################
##########################################################################





@requires_login
@app.route('/answer', methods=['POST'])
def process_answer():
    problem_num = request.form['problem_num']
    answer = request.form["answer"].strip()
    user_id = session['logged_in']

    print("form: prob_num: %s answer: %s user_id: %s" % (problem_num,answer,user_id))

    ## see if the user has answered this problem already,
    ## and let them know if they have
    completed_problems = get_completed_problems(user_id)
    if problem_num in completed_problems:
        return render_template("already_answered.html")

    ## if answer is empty string, give caustic feedback
    if answer == '':
        answer = '"No answer, just an empty void... a desolate nether."'

    ## check to see if the answer is correct
    answer_correct = check_answer(problem_num,answer)



    ## prevent users from making attepts too frequently
    overwrite = False if answer_correct else True
    time_left_to_wait = get_time_left_to_wait(user_id,overwrite)
    print("Time Left to wait: %s" % time_left_to_wait)
    if time_left_to_wait > 0:
        return render_template("too_soon.html",seconds=time_left_to_wait)


    


    problems_left = None
    if answer_correct:
        mark_as_completed(problem_num,user_id)
        problems_left = len(get_incomplete_problems(user_id))

        if problems_left == 0:
            place = db.add_winner(username,time.time())
            if place == 1:
                place = '1st'
            elif place == 2:
                place = '2nd'
            elif place == 3:
                place = '3rd'
            else:
                place = str(place) + "th"
            return render_template("winner.html",place=place)



    return render_template("feedback_template.html",answer_correct=answer_correct,answer=answer,problems_left=problems_left)




#------------------------------------------------------------------------#
##########################################################################


### I dont have time to deal with this module shit. I cant get the db in a sepearate file
### and have it know where this app is for some reason. 







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
    cur = db.execute('select * from users WHERE username = ? AND hashed_password = ?;',[username,hashed_pass])
    users = cur.fetchall()
    test_users = db.execute('select * from users;').fetchall()
    # print("test_users:",test_users)
    # for test_user in test_users:
    #     print(test_user['username'],test_user['hashed_password'])
    # print("users:%s" % str(users))
    if len(users):
        return users[0]['user_id']
    else:
        return False


### Getting problem information
###############################


def get_completed_problems(user_id):
    db = get_db()
    cur = db.execute('select * from progress where user_id = ?;', [user_id])
    problems = [row['problem_num'] for row in cur.fetchall()]
    print("completed problems:", problems)

    return problems

def get_incomplete_problems(user_id):
    db = get_db()
    cur = db.execute('select * from problems')
    all_problems = [row['problem_num'] for row in cur.fetchall()]
    completed_problems = get_completed_problems(user_id)
    incomplete_problems = [prob for prob in all_problems if prob not in completed_problems]
    # incomplete_problems.sort()
    return incomplete_problems

def get_problem_answer(problem_num):
    db = get_db()
    cur = db.execute('select * from problems where problem_num = ?',[problem_num])
    problem_answer = cur.fetchall()[0]['problem_answer']
    return str(problem_answer)

def check_answer(problem_num,answer):
    correct_answer = get_problem_answer(problem_num)
    return str(answer) == str(correct_answer)





### Answering questions
#######################

def get_time_left_to_wait(user_id,overwrite=True):
    db = get_db()
    cur = db.execute('select time_last_attempt from users where user_id = ?',[user_id])
    time_last_attempt = cur.fetchall()[0]['time_last_attempt']
    print(time_last_attempt)
    current_time = time.time()
    diff = int(current_time - time_last_attempt)
    if diff < 30:
        return 30 - diff
    else:
        if overwrite:
            cur = db.execute('update users set time_last_attempt = ? where user_id = ?;',[current_time,user_id])
            db.commit()
        return 0
        ### change value of time_last_attempt to current_time

def mark_as_completed(problem_num,user_id):
    time_finished = time.time()
    db = get_db()
    cur = db.execute(
        'insert into progress (problem_num,user_id,time_finished) values (?,?,?)',
        [problem_num,user_id,time_finished]
    )
    cur = db.execute('select points from users where user_id = ?', [user_id])
    user_points = cur.fetchall()[0]['points']

    cur = db.execute('select problem_points from problems where problem_num = ?',[problem_num])
    problem_points = cur.fetchall()[0]['problem_points']

    cur = db.execute('update users set points = ? where user_id = ?',[user_points + problem_points, user_id])

    db.commit()

#####

def get_name(user_id):
    db = get_db()
    cur = db.execute('select username from users where user_id = ?',[user_id])
    return cur.fetchall()[0]['username']


if __name__ == '__main__':
    app.run(host='0.0.0.0')
