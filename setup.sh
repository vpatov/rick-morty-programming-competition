pip install flask_navigation
pip install gunicorn 

export FLASK_APP='rmcontest'
export RMCONTEST_ROOT=$(pwd)
export PYTHONPATH="$RMCONTEST_ROOT/rmcontest/rmcontest:$PYTHONPATH"
