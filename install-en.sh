#!/bin/bash
# install mysql、redis and running
sudo apt-get install mysql-server
sudo apt-get install redis-server
sudo service redis-server start

# create database
read -r -p "please input database hostname:" hostname
read -r -p "please input database port:" port
read -r -p "please input database username:" db_username
read -r -p "please input database password:" db_password
db_name='blog'

LOGIN_CMD="mysql -h${hostname} -P${port} -u${db_username} -p${db_password}"


echo "${LOGIN_CMD}"

# 创建数据库
create_database() {
    echo "create database ${db_name}"

    create_db_sql="CREATE DATABASE IF NOT EXISTS ${db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
    echo "${create_db_sql}" | ${LOGIN_CMD}

    if [ $? -ne 0 ]
    then
        echo "create database ${db_name} failed..."
        exit 1
    else
        echo "succeed to create database ${db_name}"
    fi
}

create_database
read -r -p "是否输入.env文件关键信息(需要准备好相关信息)? [Y/n] " input

if [ "$input" == Y -o "$input" == y ]; then
      read -r -p "please input email server:" mail_server
      read -r -p "please input email username:" mail_username
      read -r -p "please input email server key:" mail_key
      read -r -p "please input CORS secret:" secret
      read -r -p "please input github client id:" github_client_id
      read -r -p "please input github client secret:" github_client_secret
      read -r -p "please input gitee client secret:" gitee_client_id
      read -r -p "please input gitee client secret:" gitee_client_secret
    else
      echo "Skip this step for .env file..."
fi

# create .env file and write value with user input
if [ "$input" == y -o "$input" == Y ]; then
cat>.env<<EOF
MAIL_SERVER=$mail_server
MAIL_USERNAME=$mail_username
MAIL_PASSWORD=$mail_key
SECRET_KEY=$secret
DATABASE_USER=$db_username
DATABASE_PWD=$db_password
BAIDU_TRANS_APPID=''
BAIDU_TRANS_KEY=''
GITHUB_CLIENT_ID=$github_client_id
GITHUB_CLIENT_SECRET=$github_client_secret
GITEE_CLIENT_ID=$gitee_client_id
GITEE_CLIENT_SECRET=$gitee_client_secret
EOF
    else
cat>.env<<EOF
 MAIL_SERVER=''
 MAIL_USERNAME=''
 MAIL_PASSWORD=''
 SECRET_KEY=''
 DATABASE_USER=$db_username
 DATABASE_PWD=$db_password
 BAIDU_TRANS_APPID=''
 BAIDU_TRANS_KEY=''
 GITHUB_CLIENT_ID=''
 GITHUB_CLIENT_SECRET=''
 GITEE_CLIENT_ID=''
 GITEE_CLIENT_SECRET=''
EOF
fi

echo 'copy config.ini file...'
cp res/config.example res/config.ini
echo 'copy config.ini file done.'

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask initdb
flask admin
flask run
