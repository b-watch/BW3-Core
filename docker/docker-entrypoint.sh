#!/bin/sh

if [ -n "$CONFIG_SERVER" ]; then
    echo "$CONFIG_SERVER" > /opt/boswatch/config/server.yaml
    exec "$@"
elif [ -n "$CONFIG_CLIENT" ]; then
    /usr/bin/pulseaudio -n -F /etc/pulse/boswatch.pa -D
    echo "$CONFIG_CLIENT" > /opt/boswatch/config/client.yaml
    exec "$@"
else
    exec "$@"
fi