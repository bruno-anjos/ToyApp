#!/bin/bash

systemctl stop mariadb
rm -rf /var/lib/mysql

mkdir  /var/lib/mysql
mount -t tmpfs -o size=2512m tmpfs /var/lib/mysql/
chmod -R 600 /var/lib/mysql
chown -R mysql:mysql /var/lib/mysql
systemctl start mariadb
