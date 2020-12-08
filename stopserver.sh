#!/bin/sh
d=''
d=`ps -ef | grep httpserver | awk 'NR==1 {print $2}'`
kill -9 $d


