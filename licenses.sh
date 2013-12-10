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

set -e

case "$1" in
  start)
        $CMD
        ;;
  stop)
        kill ` ps ax | grep runserver  | grep -v grep | awk '{ print $1}' `

        ;;
  reload|restart|force-reload|status)
        ;;
  *)
        echo "Usage: $CMD {start|stop|restart|force-reload|status}" >&2
        exit 1
        ;;
esac