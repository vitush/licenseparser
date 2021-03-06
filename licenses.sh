#! /bin/sh

### BEGIN INIT INFO
# Provides:          licenses
# Required-Start:    $local_fs $remote_fs
# Required-Stop:
# X-Start-Before:
# Default-Start:     3 4 5
# Default-Stop:
# Short-Description: Licenses Management tool
# Description: Licenses Management tool.
### END INIT INFO

CMD='python ./manage.py runserver 0.0.0.0:8000'
CMDDB='python ./manage.py syncdb'

set -e

case "$1" in
  start)
        pid=`ps ax | grep runserver  | grep -v grep | awk '{ print $1}'`
        if [ "x$pid" != "x" ]
        then
            echo Process already running with PID = $pid
        else
            $CMD  > /tmp/licenses.log  2>&1  &
            echo Started
        fi

        ;;
  stop)
        kill ` ps ax | grep runserver  | grep -v grep | awk '{ print $1}' `
        ;;
  restart)
        sh ./$0 stop
        sh ./$0 start
        ;;
  recreatedb)
        rm ./database/licenses.db
        $CMDDB
        ;;
  createdb)
        $CMDDB
        ;;
  update)
        git pull
        ;;
  status)
        pid=`ps ax | grep runserver  | grep -v grep | awk '{ print $1}'`
        [ "x$pid" != "x" ] && echo Process running with PID = $pid
        [ "x$pid" == "x" ] && echo Process stopped

        ;;
  reload|restart|status)
        ;;
  *)
        echo "Usage: $0  {start|stop|restart|status|createdb|recreatedb|update}" >&2
        exit 1
        ;;
esac