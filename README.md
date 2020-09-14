[![Build Status](https://travis-ci.org/swifty94/jarvis.svg?branch=master)](https://travis-ci.org/swifty94/jarvis)

# Jarvis

Server | PC | Laptop health analysis-tool written in Python
---

Demo application on AWS.:
------
http://jarvis.swifty94-demo-dev.xyz:5000/

- Tests passed on AWS + Travis CI (each push to master).
- Continuous Delivery by Jenkins (each push to master -> if validated > upgrade app served for demo).

Available data and statistics:
----
- General OS information (node name, OS type, arch type, etc.)  
- CPU (Number of cores, model, frequency, the temperature on the core(not supported option on Windows due to psutil library limitation and might be not available by default on some models/OS)  
- RAM (Total, used and free amount of actual RAM and swap)  
- Network (Amount of sent and received MB and packets)  
- Hard drive (Total, used and free amount on the hard drive)  
- Current processes running sorted by CPU usage + displaying RAM usage + path of the process (if can be obtained, there are bugs in Windows)  
- Thresholds dynamically highlighting if CPU usage is <= 15%, <= 60% and > 60% of CPU usage
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/cputableh.png)  
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/proch.png)


### Data is representing statistics and its graphical view on the graphs and tables based on data stored in the database and written in there by programm itself.
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/graph.png)  
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/graph2.png)  
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/graph3.png)  


### Time-based options for each KPI: latest for today, this week, this month, previous week, the previous month.

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

- Python 3.X. with the latest libs, dependencies, etc.
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

Usage:
==============

Example of installation and start of application on Ubuntu server 18.01 LTS.
---
NOTE: If the virtual environment and required dependencies do not exist, it will be installed and set automatically.

- ``` git clone https://github.com/swifty94/jarvis.git ```  
- ``` cd jarvis ```  
- ``` mysql -uroot -p'you_root_pass' < jarvis_schema.sql ```
- ``` bash bin/jarvis.sh start ```  
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/applicationstart.png)

- You can validate the application start in the application.log file:
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/applicationlog.png)
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/applicationlog2.png)

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

![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/winimpoprt.png)

- Create virtual environment and install dependecies. Example from CMD:  

``` cd C:\Users\Administrator\AppData\Local\Programs\Python\Python38\```  
``` python.exe -m venv C:\Users\Administrator\Downloads\jarvis\venv ```  
``` cd Scripts ```  
``` pip3.exe install -r C:\Users\Administrator\Downloads\jarvis\requirements.txt ```  

- Please adjust the bin/jarvis.bat file in any text editor you use
- Change SET PYTHON= and SET JARVIS_HOME= variables with the location of your Python installation and location of the Jarvis app folder.
- Example:  

![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/jarvisbat.png)

- In order to start the Jarvis server run bat file as administrator  

![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/winstart.png)  

![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/winruning.png)

- You can validate application start in application.log file:  

![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/winlog.gif)

Web-browser view:
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