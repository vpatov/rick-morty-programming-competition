from flask import Flask, request, redirect, url_for, abort, \
     render_template, Response, session
from flask_navigation import Navigation
from functools import wraps
import problems # local
import time
import os
from hashlib import sha1


app = Flask(__name__) # create the application instance :)
import database_helper as dbh
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

# def requires_auth(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth = request.authorization

#         if not auth:
#             return authenticate()

#         authorized, reason = db.check_auth(auth.username,auth.password)
#         if not authorized:
#             return authenticate()

#         return f(*args, **kwargs)
#     return decorated

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
        success = dbh.authenticate_user(username,hashed_pass)

        if success:
            session['logged_in'] = success
            return render_template('index.html',logged_in=True)
        else:
            return render_template('index.html',logged_in=False,error=True)


    else:
        print("")
    pass

def logout():
    pass

#------------------------------------------------------------------------#
##########################################################################


##########################################################################
############################### VIEWS ####################################
##########################################################################




@app.route('/')
def home_page():
    logged_in = True
    if not session.get('logged_in'):
        logged_in = False
    return render_template('index.html',logged_in=logged_in)


@app.route('/utilities')
@requires_login
def utilities_page():
    return render_template('utilities.html')




@app.route('/problems')
@requires_login
def problems_page():
    print(session['logged_in'])
    return "abc"
    completed_problems = list(db.get_progress(username).keys())
    completed_problems.sort()
    uncompleted_problems = [i for i in [1,2,3] if str(i) not in completed_problems]
    return render_template(
        'problems.html',
        uncompleted_problems=uncompleted_problems,
        completed_problems=completed_problems
        )


@requires_login
@app.route('/problem<problem_num>')
def problem_page(problem_num,no_answer=False):
    return render_template("problem" + str(problem_num) + '.html',no_answer=no_answer)



    









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
    username = request.authorization['username']

    progress = db.get_progress(username)
    if problem_num in progress:
        return render_template("already_answered.html")
    if answer == '':
        answer = '"No answer, just an empty void... a desolate nether."'

    time_left_to_wait = db.mark_attempt(username)
    print("Time Left to wait: %s" % time_left_to_wait)
    if time_left_to_wait:
        return render_template("too_soon.html",seconds=time_left_to_wait)

    correct_answer = str(db.get_problem_answer(problem_num))
    answer_correct = correct_answer == answer

    problems_left = None
    if answer_correct:
        problems_left = db.mark_as_completed(username,problem_num)

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



def winner(username):
    current_time = time.time()


#------------------------------------------------------------------------#
##########################################################################


@app.cli.command('initdb')
def init_db():
    """Initializes the database."""
    db = dbh.get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    print('Initialized the database.')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
