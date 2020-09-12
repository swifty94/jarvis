[![Build Status](https://travis-ci.org/swifty94/jarvis.svg?branch=master)](https://travis-ci.org/swifty94/jarvis)

# Jarvis

analysis-tool

Requirements
========

- Python 3.X. Windows users can download here: https://www.python.org/downloads/windows/
              Linux users, please do:
.. code-block:: shell
sudo apt update -y && sudoapt upgrade -y 
sudo apt install python3 python3-venv python3-dev python3-pip libpng-dev libfreetype6-dev -y

- MySQL 5.7: https://dev.mysql.com/downloads/mysql/5.7.html

Example usages
==============

Example of installation and start of application on Ubuntu server 18.01 LTS.
Tests passed on AWS + Travis CI
---
.. code-block:: shell
git clone https://github.com/swifty94/jarvis.git
cd jarvis
bash bin/jarvis start|stop|restart|check

master@devnull:~/Dev/jarvis_release$ bash bin/jarvis.sh
Jarvis server: NOTE: usage example:

user@host:~/jarvis_home ./jarvis start

available options: start, stop, restart, check

Windows users:
----
Please adjust bin/jarvis.bat file in any text editor you use
Change SET PYTHON= and SET JARVIS_HOME= variables with location of your Python installation and location of the jarvis app folder. Example:

![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/jarvisbat.png)


Demo application on AWS.:
------
http://jarvis.swifty94-demo-dev.xyz:5000/


Example output in web
==============

Dashboard
----
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/dashboard.png)
---
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/dashboard_2.png)

Network
----
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/network.png)

Processes
----
![](https://raw.githubusercontent.com/swifty94/jarvis/master/img/processes.png)