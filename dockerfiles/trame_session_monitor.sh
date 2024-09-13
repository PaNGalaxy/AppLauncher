#!/bin/sh
### BEGIN INIT INFO
# Provides:          <NAME>
# Required-Start:    $local_fs $network $named $time $syslog
# Required-Stop:     $local_fs $network $named $time $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Description:       <DESCRIPTION>
### END INIT INFO

SCRIPT="python /opt/trame/trame_session_monitor.py --user trame-user --target /opt/trame/session_ports --watch /opt/trame/proxy-mapping.txt --refresh 30"
RUNAS=root

PIDFILE=/var/run/trame_session_monitor.pid
LOGFILE=/var/log/trame_session_monitor.log

start() {
  if [ -f /var/run/$PIDNAME ] && kill -0 $(cat /var/run/$PIDNAME); then
    echo 'Trame Session Monitor Service already running' >&2
    return 1
  fi
  echo 'Starting Trame Session Monitor service…' >&2
  local CMD="$SCRIPT &> \"$LOGFILE\" & echo \$!"
  su -c "$CMD" $RUNAS > "$PIDFILE"
  echo 'Trame Session Monitor Service started' >&2
}

stop() {
  if [ ! -f "$PIDFILE" ] || ! kill -0 $(cat "$PIDFILE"); then
    echo 'Trame Session Monitor Service not running' >&2
    return 1
  fi
  echo 'Stopping Trame Session Monitor service…' >&2
  kill -15 $(cat "$PIDFILE") && rm -f "$PIDFILE"
  echo 'Trame Session Monitor Service stopped' >&2
}

uninstall() {
  echo -n "Are you sure that you want to uninstall this Trame Session Monitor service? That cannot be undone. [yes|No]"
  local SURE
  read SURE
  if [ "$SURE" = "yes" ]; then
    stop
    rm -f "$PIDFILE"
    echo "Notice: log file is not be removed: '$LOGFILE'" >&2
    update-rc.d -f <NAME> remove
    rm -fv "$0"
  fi
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    stop
    start
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|uninstall}"
esac