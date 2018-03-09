echo "Starting mysql service"
service mysql start
echo "initializing database"
mysql < DB_script.sql