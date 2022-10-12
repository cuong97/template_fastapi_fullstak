#!/bin/sh

BASEDIR=$(dirname "$0")
echo "$BASEDIR"

PRE_START_PATH=${PRE_START_PATH:-$BASEDIR/prestart.sh}
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    . "$PRE_START_PATH"
else
    echo "There is no script $PRE_START_PATH"
fi

export APP_MODULE=${APP_MODULE-main:app}
echo $APP_MODULE
export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-8000}

# run gunicorn
exec uvicorn $APP_MODULE --reload --workers 1 --host $HOST --port $PORT