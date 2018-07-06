#!/bin/bash

echo "Starting mysql service"
echo "port = ${4}" >> /etc/mysql/my.cnf

chmod 777 /var/lib/mysql

/etc/init.d/mysql start
echo "initializing database"
mysql < DB_script.sql

echo "starting dummy app"
python3 toyapp.py $1 $2 $3 $4 $5 
