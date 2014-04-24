#!/bin/bash
set -e
LOGFILE=/opt/balder/guni.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=8
USER=ubuntu
GROUP=ubuntu
ADDRESS=127.0.0.1:8010
cd /opt/balder
source /opt/balder/venv/bin/activate
test -d $LOGDIR || mkdir -p $LOGDI
#export NEW_RELIC_CONFIG_FILE=newrelic.ini
exec gunicorn balder.wsgi:application -w $NUM_WORKERS --bind=$ADDRESS \
  --user=$USER --group=$GROUP --log-level=debug \
  --log-file=$LOGFILE 2>>$LOGFILE