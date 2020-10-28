# Blogin
使用flask搭建的个人博客网站2.0版本，1.0版本已经停止更新。
#### 开始
##### 依赖安装
1. 安装MySQL
    进入MySQL或者mariaDB官网下载对应系统的安装包，进行安装即可。Linux用户可以通过命令进行安装`sudo apt-get install mysql`

2. 安装redis

   进入redis官网下载安装包进行安装，Linux用户可以通过下面的命令安装

   ```bash
   sudo apt-get install redis
   ```

   安装成功之后，通过如下命令开启redis服务

   ```bash
   sudo service redis-server start
   ```

3. 创建数据库

   打开终端，输入如下命令进入MySQL控制台，具体命令根据你自己的MySQL数据库的设置而定

   ```bash
   sudo mysql -u root -p
   ```

   ```mysql
   create database blog CHARACTER SET utf8 COLLATE utf8_general_ci;
   SHOW DATABASES ;
   ```

   如果控制台输出的内容中包含有`blog`数据库，则说明数据库创建成功了。
##### 初始化

1. 克隆仓库代码

   进行这一步本地机器上必须先配置好git环境，具体细节请网上冲浪查询。

   ```bash
   git clone https://github.com/weijiang1994/Blogin.git
   ```

2. 配置环境变量

   项目中有很多属性属于是私人保密属性，因此我们可以将这些属性的值保存到`.env`文件中，在上传代码的时候，将该文件屏蔽。

   在项目的根目录中新建`.env`文件，在文件中输入如下内容

   ```ini
   MAIL_SERVER='your mail server'
   MAIL_USERNAME='your mail username'
   MAIL_PASSWORD='your mail server verify code' # 不是你的邮箱密码,是申请的邮箱秘钥
   SECRET_KEY='your project secret'
   DATABASE_USER='your mysql/mariaDB database connect username'
   DATABASE_PWD='your mysql/mariaDB database connect user password'
   # 百度翻译apiid 以及 key
   BAIDU_TRANS_APPID='your app id for baidu trans'
   BAIDU_TRANS_KEY='your app key for baidu trans'
   # github第三方登录id以及key
   GITHUB_CLIENT_ID='your github client id'
   GITHUB_CLIENT_SECRET='your github client secret'
   ```

   **邮件服务器可以申请QQ邮箱或者163邮箱，具体申请流程请网上冲浪，十分简单，这里不做描述。**

3. 创建并激活虚拟环境

   由于每个项目的依赖都不一样，Python提供了虚拟环境工具来隔离每个项目的依赖，使用如下命令进行虚拟环境创建。

   ```shell
     cd Blogin
     python3 -m venv venv
   ```

   然后使用如下命令进行虚拟环境激活。

   ```shell
   source venv/bin/activate
   ```

   在Windows下激活

   ```shell
     venv\Scripts\activate
   ```

4. 安装Python依赖

   我们进入了虚拟环境以后可以使用如下命令安装第三方依赖

   ```shell
     cd Blogin
     pip install -r requirments.txt -i https://pypi.douban.com/simple
   ```

5. 初始化数据库

   进入项目的根目录，使用如下命令进行数据库初始化

   ```bash
   cd Blogin
   flask admin
   ```

6. 运行

   ```bash
   flask run
   ```

   - 打开 http://127.0.0.1:5000 就可以看到页面了。
   
   - 在线演示地址: http://2dogz.cn
   
7. issue

   如果在运行过程中有任何问题出现，欢迎issue~
