#!/bin/sh
# kill framework and friends
/etc/init.d/framework stop
kill $(pmap 2>/dev/null | grep webreader | awk '{print $1}') 2>/dev/null
kill $(pmap 2>/dev/null | grep browserd | awk '{print $1}') 2>/dev/null
kill $(pmap 2>/dev/null | grep cvm | awk '{print $1}') 2>/dev/null

# wait a moment
sleep 2

# launch dashboard
cd /mnt/us/dashboard
python3 app/main.py &
