#!/bin/bash
set -e
LOGFILE=/home/frecar/webapps/fresno/guni.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=2
USER=ubuntu
GROUP=ubuntu
ADDRESS=127.0.0.1:8013
cd /home/frecar/webapps/fresno/
source /home/frecar/webapps/fresno/bin/activate
test -d $LOGDIR || mkdir -p $LOGDI
#export NEW_RELIC_CONFIG_FILE=newrelic.ini
exec gunicorn -w 4 -b 127.0.0.1:8012 fresno:app