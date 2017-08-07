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
        print("AUTH:",auth)

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
    nav.Item('Problems','problems')
    # nav.Item('Latest News', 'news', {'page': 1}),
])


# @app.route('/news/<int:page>')
# def news(page):
#     return render_template('news.html', page=page)


#------------------------------------------------------------------------#
##########################################################################




@app.route('/problems')
@requires_auth
def problems():
    return render_template('problems.html',problems=[1,2,3])


@app.route('/')
@requires_auth
def home_page():
    return render_template('index.html')


@app.route('/utilities')
@requires_auth
def utilities_page():
    return render_template('utilities.html')



@app.route('/problem<problem_num>')
def problem_page(problem_num):
    return render_template("problem" + str(problem_num) + '.html')

@app.route('/answer', methods=['POST'])
def process_answer():
    return "You answered %s to problem %s" % (request.form["answer"],request.form["problem_num"])

if __name__ == '__main__':
    app.run(host='0.0.0.0')
