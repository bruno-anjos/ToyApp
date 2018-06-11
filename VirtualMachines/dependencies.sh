#!/bin/bash

yum install -y http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm 
yum update -y
yum install -y mysql 
yum install -y mysql-devel 
yum install -y mariadb-server
yum install -y python34-devel
yum install -y python34-setuptools
yum install -y git
yum install -y gcc

sudo easy_install-3.4 pip
pip3 install mysqlclient
if [ ! -d "/root/ToyApp" ]; then
    git clone https://github.com/bruno-anjos/ToyApp.git
fi
cd /root/ToyApp && git pull && cd ..

bash /root/ToyApp/VirtualMachines/install_ramdisk.sh
