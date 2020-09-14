[![Build Status](https://travis-ci.org/swifty94/jarvis.svg?branch=master)](https://travis-ci.org/swifty94/jarvis)

# Jarvis

analysis-tool

App stack:
========
- Python:
    - Psutil - KPI collection from OS API
    - Matplotlib - data visualization
    - Flask - web-framework
    - Multiprocessing 
    - Waitress - WSGI webserver
- MySQL
- HTML\Jinja2
- CSS\JS

Requirements
========

- Python 3.X. Windows users can download here: https://www.python.org/downloads/windows/
Linux users, please do:

sudo apt update -y && sudoapt upgrade -y 
sudo apt install python3 python3-venv python3-dev python3-pip libpng-dev libfreetype6-dev -y

- MySQL 5.7: https://dev.mysql.com/downloads/mysql/5.7.html

Example usages
==============

Example of installation and start of application on Ubuntu server 18.01 LTS.
---
Tests passed on AWS + Travis CI
---

- ``` git clone https://github.com/swifty94/jarvis.git ```
- ``` cd jarvis ```
- ``` bash bin/jarvis start|stop|restart|check ```

- ``` master@devnull:~/Dev/jarvis_release$ bash bin/jarvis.sh ```
- ``` Jarvis server: NOTE: usage example: ```
``` user@host:~/jarvis_home ./jarvis start ```
``` available options: start, stop, restart, check ```
Windows users:
----
- Please adjust bin/jarvis.bat file in any text editor you use
- Change SET PYTHON= and SET JARVIS_HOME= variables with location of your Python installation and location of the jarvis app folder. 
- Example:
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/jarvisbat.png)


Demo application on AWS.:
------
http://jarvis.swifty94-demo-dev.xyz:5000/


Example output in web
==============

Dashboard
----
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/dashboard.png)
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/dashboard_2.png)

RAM
---
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/ram_prev_month.png)
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/ram2.png)

CPU
---
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/cpu2.png)
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/cpu3.png)

Hard drive:
---
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/disk.png)
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/disk2.png)

Network
----
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/network.png)
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/net2.png)

Processes
----
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/processes.png)