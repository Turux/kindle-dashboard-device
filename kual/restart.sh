#!/bin/sh
kill $(ps | grep 'python3 app/main.py' | grep -v grep | awk '{print $1}') 2>/dev/null
sh /mnt/us/extensions/dashboard/start.sh
