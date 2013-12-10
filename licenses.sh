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
        $CMD  > /tmp/licenses.log  2>&1  &
        ;;
  stop)
        kill ` ps ax | grep runserver  | grep -v grep | awk '{ print $1}' `
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
        ps ax | grep runserver  | grep -v grep | awk '{ print $1}'
        RETVAL=$?
        [ $RETVAL -eq 0 ] && echo Process running with PID = $pid
        [ $RETVAL -ne 0 ] && echo Process stopped

        ;;
  reload|restart|status)
        ;;
  *)
        echo "Usage: $0  {start|stop|status|createdb|recreatedb|update}" >&2
        exit 1
        ;;
esac