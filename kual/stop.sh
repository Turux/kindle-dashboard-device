#!/bin/sh
# kill dashboard
kill $(ps | grep 'python3 app/main.py' | grep -v grep | awk '{print $1}') 2>/dev/null

# restart framework
/etc/init.d/framework start
