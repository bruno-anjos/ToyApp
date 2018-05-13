echo "starting mysql service"
service mysql start
echo "running DB script"
mysql < /root/Toyapp/Containers/Container/DB_script.sql
echo "starting toyapp....."
python3 /root/Toyapp/Containers/Container/toyapp.py
echo "erasing DB"
mysql < erase_DB.sql