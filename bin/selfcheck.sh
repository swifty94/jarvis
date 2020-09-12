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
    echo "HTTP request to $i endpoint"
    response=$(curl -s -I $URL/$i | grep HTTP/1.1 | awk {'print $2'})
    echo $response >> tmp.log
    echo ''
    echo "HTTP response from $i - $response"
done

INTSERVER=$(grep -ic 500 tmp.log)
NOTFOUND=$(grep -ic 404 tmp.log)
NOPERMISSIONS=$(grep -ic 403 tmp.log)
OK=$(grep -ic 200 tmp.log)

echo "Score:"
echo "HTTP 200: $OK"
echo "HTTP 500: $INTSERVER"
echo "HTTP 404: $NOTFOUND"
echo "HTTP 403: $NOPERMISSIONS"

if [ $NOPERMISSIONS -ne 0 ]; then
    echo "Result:"
    echo "HTTP ERROR while hook to UI"
    echo "Post-deploy tests FAILED"
    exit 1
elif [ $NOTFOUND -ne 0 ]; then
    echo "Result:"
    echo "HTTP ERROR while hook to UI"
    echo "Post-deploy tests FAILED"
    exit 1
elif [ $INTSERVER -ne 0 ]; then
    echo "Result:"
    echo "HTTP ERROR while hook to UI"
    echo "Post-deploy tests FAILED"
else
    echo "Result:"
    echo "UI hooks OK"
    echo "Post-deploy tests passed"
fi
rm -f tmp.log