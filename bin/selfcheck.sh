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
    response=$(curl -s -I $URL/$i | grep HTTP/1.1 | awk {'print $2'})
    echo $response >> tmp.log
done

INTSERVER=$(grep -ic 500 tmp.log)
NOTFOUND=$(grep -ic 404 tmp.log)
NOPERMISSIONS=$(grep -ic 403 tmp.log)

if [ $NOPERMISSIONS -ne 0 ]; then
    echo "HTTP ERROR while hook to UI"
    echo "BUILD FAILED"
    exit 1
elif [ $NOTFOUND -ne 0 ]; then
    echo "HTTP ERROR while hook to UI"
    echo "BUILD FAILED"
    exit 1
elif [ $INTSERVER -ne 0 ]; then
    echo "HTTP ERROR while hook to UI"
    echo "BUILD FAILED"
else
    echo "UI hooks OK"
    echo "POSR-DEPLOY TEST PASSED"
fi

rm -f tmp.log
