NUM_WORKERS=12
TIMEOUT=10000


gunicorn  \
--workers $NUM_WORKERS \
--timeout $TIMEOUT \
--log-level=info \
--bind=0.0.0.0:5000 \
wsgi
