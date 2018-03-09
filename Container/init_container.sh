echo "Starting mysql service"
service mysql start
echo "initializing database"
mysql < DB_script.sql

echo "starting dummy app with $1 InsPerMin and $2 timeout"
python3 toyapp.py $1 $2 > toyapp.log