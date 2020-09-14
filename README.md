[![Build Status](https://travis-ci.org/swifty94/jarvis.svg?branch=master)](https://travis-ci.org/swifty94/jarvis)

# Jarvis

analysis-tool

Demo application on AWS.:
------
http://jarvis.swifty94-demo-dev.xyz:5000/

- Tests passed on AWS + Travis CI (each push to master). 
- Continuosus delivery by Jenkins (each push to master -> if validated > upgrade app served for demo).

App stack:
========
- Python:
    - Psutil - KPI collection from OS API. https://psutil.readthedocs.io/en/latest/
    - Matplotlib - data visualization. https://matplotlib.org/
    - Flask - web-framework https://flask.palletsprojects.com/en/1.1.x/
    - Multiprocessing https://docs.python.org/3/library/multiprocessing.html
    - Waitress - WSGI webserver https://docs.pylonsproject.org/projects/waitress/en/stable/
- MySQL
- HTML\Jinja2
- CSS\JS

Requirements
========

- Python 3.X. with latests libs, dependecies etc. 
    - Linux users (verified on Ubuntu 18.04, other distros must use their packet managers, e.g. yum, dnf, etc.):
    ``` sudo apt update -y && apt upgrade -y ```  
    ``` sudo apt install python3 python3-venv python3-dev python3-pip libpng-dev libfreetype6-dev -y ```  
    - Windows users can download here: https://www.python.org/downloads/windows/

- MySQL 5.7: 
    - Linux users (verified on Ubuntu 18.04, other distros must use their packet managers, e.g. yum, dnf, etc. and/or adjust repositories to download 5.7 instead of 8.0):
   ```sudo apt install mysql-server -y ```  
   ```sudo systemctl start mysql ```  
   ```mysql_secure_installation ```  
    - Windows users go here: https://dev.mysql.com/downloads/mysql/5.7.html

Example usages
==============

Example of installation and start of application on Ubuntu server 18.01 LTS.
---
NOTE: If virtual environment and required dependencies does not exists, it will be installed and set automatically.

- ``` git clone https://github.com/swifty94/jarvis.git ```  
- ``` cd jarvis ```  
- ``` mysql -uroot -p'you_root_pass' < jarvis_schema.sql ```
- ``` bash bin/jarvis.sh start ```  
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/applicationstart.gif)

- You can validate application start in application.log file:
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/applicationlog.gif)

- Available options to interract with jarvis.sh script:
``` master@devnull:~/Dev/jarvis_release$ bash bin/jarvis.sh ```  
``` Jarvis server: NOTE: usage example: ```  

``` user@host:~/jarvis_home ./jarvis start ```  

``` available options: start, stop, restart, check ```  
Example with restart + selfcheck option to validate HTTP 200 OK reply from UI endpoints:
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/applicationcheck.gif)

Windows users:
----
- ``` git clone https://github.com/swifty94/jarvis.git ```
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/wingit.png)
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/wingit2.png)
- ``` cd C:\Program Files\MySQL\MySQL Server 5.7\bin\ ```
- ``` mysql.exe -uroot -p C:\Users\Administrator\Downloads\jarvis_schema.sql ```
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/winimport.png)

- Create virtual environment and install dependecies. Example from CMD:
```cd C:\Users\Administrator\Downloads\jarvis```  
``` C:\Users\Administrator\AppData\Local\Programs\Python\Python38\python3 -m venv venv ```  
``` C:\Users\Administrator\AppData\Local\Programs\Python\Python38\Scripts\pip3 install -r requirements. txt ```  
- Please adjust bin/jarvis.bat file in any text editor you use
- Change SET PYTHON= and SET JARVIS_HOME= variables with location of your Python installation and location of the jarvis app folder. 
- Example:
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/jarvisbat.png)

- In order to start the Jarvis server run bat file as administrator
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/winstart.png)
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/winrunning.png)

- You can validate application start in application.log file:
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/winlog.gif)

Example output in web
==============

Dashboard
----
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/dashboard.png)
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/dashboard_2.png)
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/windowsdashboard.png)

RAM
---
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/ram_prev_month.png)
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/ram2.png)

CPU
---
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/cpu2.png)
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/cpu3.png)
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/wincpug.png)

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