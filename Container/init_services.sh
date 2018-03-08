#!/bin/bash


echo "Starting services"

cd /app
service mysql start 
mysql < init_sql.sql
python3 toyapp.py