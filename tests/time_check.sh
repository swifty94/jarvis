#!/bin/bash
############################################################
#
#
#	Checking time of reply back from application
#
#
############################################################
echo 'Time to deliver dashboard page'
echo ''
time curl -I http://127.0.0.1:8080/ > /dev/null 2>&1
echo ''
echo 'Time to deliver cpu page...'
echo ''
time curl -I http://127.0.0.1:8080/cpu_stats > /dev/null 2>&1
echo ''
echo 'Time to deliver disk page...'
echo ''
time curl -I http://127.0.0.1:8080/disk_stats > /dev/null 2>&1
echo ''
echo 'Time to deliver ram page...'
echo ''
time curl -I http://127.0.0.1:8080/net_stats > /dev/null 2>&1
echo ''
echo 'Time to deliver net page...'
echo ''
time curl -I http://127.0.0.1:8080/ram_stats > /dev/null 2>&1
echo ''
echo 'Time to deliver processes page...'
echo ''
time curl -I http://127.0.0.1:8080/processes > /dev/null 2>&1
echo ''