#!/bin/bash

#echo deb http://http.debian.net/debian jessie-backports main >> /etc/apt/sources.list

echo "--------------------------UPDATING----------------------------"
apt-get update

echo "--------------------------DOWNLOADING PYTHON----------------------------"
apt-get install -y python3.5


echo "--------------------------DOWNLOADING python3-mysqldb----------------------------"
apt-get install -y python3-mysqldb

echo "--------------------------DOWNLOADING mysql-server----------------------------"
apt-get install -y mysql-server


echo "--------------------------DOWNLOADING mysql-client----------------------------"
apt-get install -y mysql-client


