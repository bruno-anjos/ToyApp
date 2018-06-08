#!/bin/bash

rm -rf /var/lib/mysql/*
cp my.cnf /etc/my.cnf
mkdir /ramdisk

mount -t tmpfs -o size=1G tmpfs /ramdisk
mkdir /ramdisk/mysqldata
mkdir /ramdisk/mysqltemp

chmod -R 777 /ramdisk
chmod 600 /etc/my.cnf
chown mysql:mysql /ramdisk

