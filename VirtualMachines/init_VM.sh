echo "starting mysql service"
service mysql start
echo "running DB script"
mysql < ../Containers/Container/DB_script.sql
echo "starting toyapp....."
cd ../Containers/Container
python3 toyapp.py
cd ../../VirtualMachines
echo "erasing DB"
mysql < erase_DB.sql