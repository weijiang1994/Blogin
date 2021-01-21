#!/bin/bash
#sudo apt-get install mysql-server-5.7
#sudo apt-get install redis-server
#sudo service redis-server start
read -p "please input mysql hostname:" hostname
read -p "please input mysql port:" port
read -p "please input mysql username:" db_username
read -p "please input mysql password:" db_password
db_name = 'blog'

LOGIN_CMD="mysql -h${hostname} -P${port} -u${db_username} -p${db_password}"


echo ${LOGIN_CMD}

# 创建数据库
create_database() {
    echo "create database ${db_name}"

    create_db_sql="CREATE DATABASE IF NOT EXISTS ${db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
    echo ${create_db_sql} | ${LOGIN_CMD}


    if [ $? -ne 0 ]
    then
        echo "create database ${db_name} failed..."
        exit 1
    else
        echo "succeed to create database ${db_name}"
    fi
}

create_database
read -p "please input mail server" mail_server
read -p "please input mail username" mail_username
read -p "please input mail server key" mail_key
read -p "please input crsf secret" secret


git clone https://github.com/weijiang1994/Blogin.git
cd Blogin
python3 -m venv venv
source venv/bin/activate
pip install -r requirments.txt -i https://pypi.douban.com/simple
flask run
