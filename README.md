# Blogin
使用flask搭建的个人博客网站2.0版本，1.0版本已经停止更新。
#### 开始
##### 依赖安装
1. 安装MySQL
进入MySQL或者mariaDB官网下载对应系统的安装包，进行安装即可。
Linux用户可以通过如下命令进行安装
```bash
sudo apt-get install mysql
```
2. 安装redis
进入redis官网下载安装包进行安装，Linux用户可以通过如下命令进行安装
```bash
sudo apt-get install redis
```
安装成功之后，通过如下命令开启redis服务
```bash
service redis-server start
```
3. 创建数据库
打开终端输入如下命令进入MySQL控制台，具体命令根据你MySQL数据库的设置而定。
```bash
sudo mysql -u root -p
```
```mysql
CREATE DATABASE blog;
SHOW DATABASES ;
```
如果控制台输出的内容中包含有`blog`数据库，则说明数据库创建成功。
##### 初始化
1. 克隆代码仓库
```bash
git clone https://github.com/weijiang1994/Blogin.git
```
​		  进行这一步本地机器必须先配置好git环境，具体细节请网上冲浪查询。
2. 配置环境变量

     在项目的根目录新建`.env`文件，在文件中输入如下内容:

```ini
MAIL_SERVER='your mail server'
MAIL_USERNAME='your mail username'
MAIL_PASSWORD='your mail server verify code' # not your mail password
SECRET_KEY='your project secret'
DATABASE_USER='your mysql/mariaDB database connect username'
DATABASE_PWD='your mysql/mariaDB database connect user password'
```
>邮件服务器可以申请QQ邮箱或者163邮箱，具体申请流程请网上冲浪，十分简单。
3. 创建并激活虚拟环境
由于每个项目的依赖都不一样，Python提供了虚拟环境工具来隔离每个项目的依赖，使用如下命令进行虚拟环境创建。
```bash
cd Blogin
python3 -m venv venv
```
然后使用如下命令进行虚拟环境激活
```bash
. venv/bin/activate
```
在Windows下使用如下命令激活
```bash
venv\Scripts\activate
```
4. 安装python依赖
我们进入了虚拟环境以后可以使用如下命令安装第三方依赖
```bash
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

   打开 http://127.0.0.1:5000 就可以看到页面了。