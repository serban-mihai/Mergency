#!/bin/bash

if [[${USER} ]] then
    echo "You need to run the script as ROOT"

fi

echo "Mergency Installer"

apt update
apt upgrade
apt install wget
apt install libaio1
apt instll libaio-dev

echo "May require login with an Oracle Account"
wget http://download.oracle.com/otn/linux/instantclient/11204/instantclient-basic-linux.x64-11.2.0.4.0.zip
mkdir instantclient_11_2
unzip instantclient-basic-linux.x64-11.2.0.4.0.zip instantclient_11_2

mkdir /opt/oracle
mv -r instantclient_11_2 /opt/oracle
cd /opt/oracle/

ln -s libclntsh.so.11.1 libclntsh.so
sh -c "echo /opt/oracle/instantclient_11_2 > /etc/ld.so.conf.d/oracle-instantclient.conf"
ldconfig
export LD_LIBRARY_PATH=/opt/oracle/instantclient_11_2