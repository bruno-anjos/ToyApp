#!/bin/bash

rm -rf /var/lib/mysql/*
mkdir /ramdisk

mount -t tmpfs -o size=1G tmpfs /ramdisk
mkdir /ramdisk/mysqldata
mkdir /ramdisk/mysqltemp

chmod -R 777 /ramdisk
chown mysql:mysql /ramdisk

echo "[mysqld]" >> /etc/mysql/my.cnf	
echo "innodb_use_native_aio = 0" >> /etc/mysql/my.cnf
echo "datadir = /ramdisk/mysqldata" >> /etc/mysql/my.cnf
echo "tmpdir = /ramdisk/mysqltemp" >> /etc/mysql/my.cnf