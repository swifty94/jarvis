#!/bin/bash 

URL='http://127.0.0.1:5000'

ENDPOINTS=(
"/"
"dashboard"
"cpu_stats"
"ram_stats"
"net_stats"
"disk_stats"
"processes"
)

for i in "${ENDPOINTS[@]}"; do    
    curl -s -I $URL/$i
done