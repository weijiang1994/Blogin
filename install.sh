#!/bin/bash
# 安装mysql、redis数据库并启动
sudo apt-get install mysql-server-5.7
sudo apt-get install redis-server
sudo service redis-server start

# 创建mysql数据库
read -p "请输入数据库主机名:" hostname
read -p "请输入数据库端口号:" port
read -p "请输入数据库连接用户名:" db_username
read -p "请输入数据库连接密码:" db_password
db_name='blog'

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
read -r -p "是否输入.env文件关键信息(需要准备好相关信息)? [Y/n] " input

if [ $input == Y -o $input == y ]; then
      read -p "请输入邮箱服务配置:" mail_server
      read -p "请输入邮箱服务用户名:" mail_username
      read -p "请输入邮箱服务key:" mail_key
      read -p "请输入防跨域攻击secret:" secret
      read -p "请输入github client id:" github_client_id
      read -p "请输入github client secret:" github_client_secret
    else
      echo "跳过.env文件信息输入"
fi

# 创建文件并根据用户是否输入信息来填写或者保留空值
if [ $input == y -o $input == Y ]; then
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
EOF
fi


python3 -m venv venv
source venv/bin/activate
pip install -r requirments.txt -i https://pypi.douban.com/simple
flask admin
flask run
