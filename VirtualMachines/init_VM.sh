#!/bin/bash

apt-get install python3 -y 
apt-get install python3-pip-y 
apt-get install mysql-server -y 
apt-get install mysql-client -y 
apt-get install libmysqlclient-dev -y 
pip3 install --upgrade pip 
pip3 install mysqlclient --upgrade pip

mysql < DB_script.sql