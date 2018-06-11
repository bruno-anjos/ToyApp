#!/bin/bash

rm -rf /var/lib/mysql

mkdir  /var/lib/mysql
mount -t tmpfs -o size=1G tmpfs /var/lib/mysql/
chmod -R 600 /var/lib/mysql
chown -R mysql:mysql /var/lib/mysql

