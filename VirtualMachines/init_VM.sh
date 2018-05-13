/etc/init.d/mysql start
mysql < ../Containers/Container/DB_script.sql
python3 ../Containers/Container/toyapp.py
mysql < erase_DB.sql