#! /bin/sh
###########################################
#
#       Script to start Jarvis server
#
###########################################

export JARVIS_HOME=/home/master/Dev/jarvis_1.0.2

start() {
        export now=`date +%m_%d_%H:%M:%S`
        if [  -f application.log  ]; then
                echo "Jarvis server: Log file copied to archieve in $JARVIS_HOME/log/"
                echo ''
                echo "Jarvis server: Log file name: application.log_$now"
                echo ''
                echo "Jarvis server: Old log truncated. Appending from scratch"
                echo ''
                cp application.log log/application.log_$now
                rm -f application.log
        fi
        if [  -d venv  ]; then
                echo "Jarvis server: Virtual environment already exist!"
                echo ''
                echo "Jarvis server: Activating virtual environment.."
                cd $JARVIS_HOME
                source venv/bin/activate
                echo ''
                echo "Jarvis server: DONE"
                echo ''
                echo "Jarvis server: Wake up!"
                echo ''
                echo "Jarvis server: Database worker start"
                echo ''
                echo "Jarvis server: Visual worker start"
                echo ''
                echo "Jarvis server: Web server start"
                echo ''
                echo "Jarvis server: Application start..."
                venv/bin/python3 $JARVIS_HOME/jarvis.py >> application.log &
                venv/bin/python3 $JARVIS_HOME/sql_worker.py  >> application.log &
                echo ''
                sleep 3
                echo 'Jarvis server: DONE!'
                echo ''
                echo 'Jarvis server: You can check the GUI via:'
                echo ''
                echo "http://your_domain_or_ip_address:8080/"
        else    
                cd $JARVIS_HOME
                echo "Jarvis server: Virtual environment NOT FOUND!"
                echo ''
                echo "Jarvis server: Installing virtual environment.."
                sleep 2
                python3 -m venv venv
                echo ''
                echo 'Jarvis server: DONE'
                echo ''
                echo 'Jarvis server: Activate virtual environment'
                source venv/bin/activate
                sleep 2
                echo ''
                echo 'Jarvis server: DONE'
                echo ''
                echo "Jarvis server: Installing dependencies...Hold on"
                venv/bin/pip3 install -r dependencies.txt > /dev/null 2> /dev/null && sleep 2
                echo "Jarvis server: DONE"
                echo ''
                venv/bin/python3 $JARVIS_HOME/jarvis.py >> application.log &
                venv/bin/python3 $JARVIS_HOME/sql_worker.py >> application.log &
                echo ''
                echo "Jarvis server: DONE"
                echo ''
                echo "Jarvis server: Wake up"
                echo ''
                echo "Jarvis server: Database worker start"
                echo ''
                echo "Jarvis server: Visual worker start"
                echo ''
                echo "Jarvis server: Web server start"
                echo ''
                echo "Jarvis server: Application start"
                echo ''
                sleep 3
                echo 'Jarvis server: DONE!'
                echo ''
                echo 'Jarvis server: You can check the GUI via:'
                echo ''
                echo "http://your_domain_or_ip_address:8080/"
                
        fi
}

stop() {
        export now=`date +%m_%d_%H:%M:%S`
        PID1=$(ps aux|grep -v grep|grep jarvis.py |awk '{print $2}')
        PID2=$(ps aux|grep -v grep|grep sql_worker.py |awk '{print $2}')
        echo "Jarvis server: gracefull shutdown."
        echo ''
        kill -9 $PID1
        kill -9 $PID2
        echo "Jarvis server: Received call stop() function"
        echo ''
        echo "Jarvis server: Database worker shutdown!"
        echo ''
        echo "Jarvis server: Visual worker shutdown!"
        echo ''
        echo "Jarvis server: Web server shutdown!"
        echo ''
        echo "Jarvis server: Application stoped"
        echo ''
}       

restart() {
        stop
        sleep 5
        start
}

case "$1" in
        start)
                start 
                ;;
        stop)
                stop
                ;;
        restart)
                restart
                ;;
        *)
                echo "Jarvis server: NOTE: usage example:"
                echo ''
                echo "user@host:~/jarvis_home ./jarvis start"
                echo ''
                echo "available options: start, stop, restart"
                exit 1
esac

exit 0