#pip install flask_navigation
#pip install gunicorn 

FLASK_APP='rmcontest'
RMCONTEST_ROOT=$(pwd)
PYTHONPATH="$RMCONTEST_ROOT/rmcontest/rmcontest:$PYTHONPATH"

export FLASK_APP
export RMCONTEST_ROOT
export PYTHONPATH

echo $FLASK_APP
echo $RMCONTEST_ROOT
echo $PYTHONPATH

cd rmcontest/rmcontest
flask initdb
python populate_db.py
