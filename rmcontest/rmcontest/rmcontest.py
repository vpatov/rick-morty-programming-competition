from flask import Flask, request, redirect, url_for, abort, \
     render_template, Response
	
from flask_navigation import Navigation

from functools import wraps
import db
import problems


app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , rmcontest.py




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

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization

        if not auth:
            return authenticate()

        authorized, reason = db.check_auth(auth.username,auth.password)
        if not authorized:
            return authenticate()

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




@app.route('/problems')
@requires_auth
def problems_page():
    username = request.authorization['username']
    completed_problems = list(db.get_progress(username).keys())
    completed_problems.sort()
    uncompleted_problems = [i for i in [1,2,3] if str(i) not in completed_problems]
    return render_template(
        'problems.html',
        uncompleted_problems=uncompleted_problems,
        completed_problems=completed_problems
        )


@app.route('/')
def home_page(nav=nav):
    return render_template('index.html')


@app.route('/utilities')
@requires_auth
def utilities_page():
    return render_template('utilities.html')



def winner(username):
    current_time = time.time()
    


@requires_auth
@app.route('/problem<problem_num>')
def problem_page(problem_num,no_answer=False):
    return render_template("problem" + str(problem_num) + '.html',no_answer=no_answer)

@requires_auth
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
            place = add_winner(username,time.time())




    





    return render_template("feedback_template.html",answer_correct=answer_correct,answer=answer,problems_left=problems_left)















if __name__ == '__main__':
    app.run(host='0.0.0.0')
