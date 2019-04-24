#!/bin/bash

if [[${USER} ]] then
    echo "You need to run the script as ROOT"

fi

echo "Mergency Installer"

apt update -y
apt upgrade -y
apt install wget -y
apt install libaio1 -y
apt install libaio-dev -y
apt install python3.6 -y
apt install pip3 -y

apt install xclip xsel -y
git clone https://github.com/HeaTTheatR/KivyMD.git
python3.6 KivyMD/setup.py install
rm -r KivyMD

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