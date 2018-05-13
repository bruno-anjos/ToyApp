echo "starting mysql service"
service mysql start
echo "running DB script"
mysql < ../Containers/Container/DB_script.sql
echo "starting toyapp....."
python3 ../Containers/Container/toyapp.py
echo "erasing DB"
mysql < erase_DB.sql