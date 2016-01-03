#!/usr/local/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/../api

cmd_test="/opt/venv/foodnemo/bin/python test.py"
# cmd_prod="/opt/venv/foodnemo/bin/python prod.py"

proc_test=`ps aux | grep "$cmd_test" | grep -v grep | wc -l | awk '{print $1}'`
# proc_prod=`ps aux | grep "$cmd_prod" | grep -v grep | wc -l | awk '{print $1}'`

if [ "$proc_test" -lt 1 ]; then $cmd_test; fi
# if [ "$proc_prod" -lt 1 ]; then $cmd_prod; fi
