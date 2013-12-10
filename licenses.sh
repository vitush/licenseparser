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
        $CMD  2>&1 > /dev/null &
        ;;
  stop)
        kill ` ps ax | grep runserver  | grep -v grep | awk '{ print $1}' `
        ;;
  createdb)
        $CMDDB
        ;;
  reload|restart|status)
        ;;
  *)
        echo "Usage: $0  {start|stop|createdb}" >&2
        exit 1
        ;;
esac