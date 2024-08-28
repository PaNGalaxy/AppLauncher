#!/bin/bash

mkdir -p /opt/trame/session_ports

for port in {9001..9500}
do
  if nc -z -w 1 localhost $port; then
    touch "/opt/trame/session_ports/$port"
  else
    rm -f "/opt/trame/session_ports/$port"
  fi
done