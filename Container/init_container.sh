echo "Starting mysql service"
service mysql start
echo "initializing database"
mysql < database_creation.sql