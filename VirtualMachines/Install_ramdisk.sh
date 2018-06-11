#!/bin/bash

rm -rf /var/lib/mysql/*

mount -t tmpfs -o size=1G tmpfs /var/lib/mysql/
chmod 600 /var/lib/mysql/
chown mysql:mysql /var/lib/mysql/

