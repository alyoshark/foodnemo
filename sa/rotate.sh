#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/../raw

# date_suffix=`date -v-1d +'%Y%m%d'`  # FreeBSD Style
date_suffix=`date +'%Y%m%d' -d'Yesterday'`  # Linux Style

test_rot=test-order.json-$date_suffix
mv test-order.json $test_rot

prod_rot=order.json-$date_suffix
mv order.json $prod_rot

kill -USR1 `cat /run/nginx.pid`
[ -f test-order.pid ] && kill -USR1 `cat test-order.pid`
[ -f order.pid ] && kill -USR1 `cat order.pid`

gzip $test_rot
gzip $prod_rot
