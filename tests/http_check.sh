#!/bin/bash
############################################################
#
#
#	Checking HTTP responses from the application
#
#
############################################################

DASHBOARD_RESPONSE=$(curl -ILs http://127.0.0.1:8080/| grep HTTP|awk '{print $2}')
CPU_RESPONSE=$(curl -ILs http://127.0.0.1:8080/cpu_stats| grep HTTP|awk '{print $2}')
DISK_RESPONSE=$(curl -ILs http://127.0.0.1:8080/disk_stats| grep HTTP|awk '{print $2}')
NET_RESPONSE=$(curl -ILs http://127.0.0.1:8080/net_stats| grep HTTP|awk '{print $2}')
RAM_RESPONSE=$(curl -ILs http://127.0.0.1:8080/ram_stats| grep HTTP|awk '{print $2}')
PROC_RESPONSE=$(curl -ILs http://127.0.0.1:8080/processes| grep HTTP|awk '{print $2}')


echo 'Checking dashboard page'
echo "HTTP response $DASHBOARD_RESPONSE"
echo ''
echo 'Checking cpu page'
echo "HTTP response $CPU_RESPONSE"
echo ''
echo 'Checking disk page'
echo "HTTP response $DISK_RESPONSE"
echo ''
echo 'Checking ram page'
echo "HTTP response $NET_RESPONSE"
echo ''
echo 'Checking net page'
echo "HTTP response $RAM_RESPONSE"
echo ''
echo 'Checking processes page'
echo "HTTP response $PROC_RESPONSE"
echo ''

