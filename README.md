# Blogin

![python-depend.svg](https://img.shields.io/badge/PYTHON-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue)
![stars](https://img.shields.io/github/stars/weijiang1994/blogin)
![fork](https://img.shields.io/github/forks/weijiang1994/blogin)

使用Flask+Bootstrap4开发的个人博客系统。

> 如果有帮助到你，还请金手**Star-Star-Star**一下啦，不甚感激~~~
   
在线演示地址: https://2dogz.cn

[English Document](https://github.com/weijiang1994/Blogin/blob/master/README-EN.md)
## 功能介绍

依赖于Flask Python Web框架开发的个人博客网站，包含有前台与后台两个部分。
### 前台功能介绍

<details open>
  <summary><b>1.个人博客</b></summary>
<div align="left">
    <ul>
    <li>主页展示每条博客简短介绍</li>
    <li>支持博客分类</li>
    <li>支持评论、社交网络分享</li>
    <li>支持博客归档</li>
    </ul>
</div>
</details>
<details>
  <summary><b>2.个人相册</b></summary>
<div align="left">
    <ul>
    <li>支持tag标签</li>
    <li>支持评论点赞</li>
    <li>支持社交账号分享</li>
    </ul>
</div>
</details>

<details>
  <summary><b>3.在线工具</b></summary>
<div align="left">
    <ul>
    <li>在线词云图生成工具</li>
    <li>多端翻译工具</li>
    <li>唐宋诗词查询工具</li>
    <li>在线OCR工具</li>
    <li>在线IP真实地址查询工具</li>
    </ul>
</div>
</details>

<details>
  <summary><b>4.评论系统</b></summary>
<div align="left">
    <ul>
    <li>支持评论、删除、举报功能</li>
    <li>支持评论子回复功能</li>
    </ul>
</div>
</details>

<details>
  <summary><b>5.用户个人资料(网站用户)</b></summary>
<div align="left">
    <ul>
    <li>用户个人动态展示</li>
    <li>未读消息提醒(有人回复你的评论)</li>
    <li>修改个人资料、密码</li>
    <li>登录日志记录(包括实际登录地点)</li>
    </ul>
</div>
</details>

<details>
  <summary><b>6.唐宋诗词</b></summary>
<div align="left">
    <ul>
    <li>随机显示一首唐宋诗</li>
    <li>随机显示一首宋词</li>
    <li>提供获取诗词的API接口</li>
    </ul>
</div>
</details>


<details>
  <summary><b>7.毒鸡汤文本</b></summary>
<div align="left">
    <ul>
    <li>随机一条毒鸡汤文案</li>
    <li>提供获取毒鸡汤文案的API接口</li>
    </ul>
</div>
</details>


<details>
  <summary><b>8.其他</b></summary>
<div align="left">
    <ul>
    <li>支持个人计划制定</li>
    <li>支持近三个月contribute热力图显示</li>
    <li>网站更新里程碑记录</li>
    </ul>
</div>
</details>

### 后台功能介绍

<details>
  <summary><b>1.内容管理</b></summary>
<div align="left">
    <ul>
    <p>博客管理</p>
    <ul>
        <li>新增博客</li>
        <li>编辑博客</li>
        <li>删除博客(前台屏蔽)</li>
    </ul>
    </ul>
    <ul>
    <p>相册管理</p>
    <ul>
        <li>新增照片</li>
        <li>编辑照片</li>
        <li>删除照片(前台屏蔽)</li>
    </ul>
    </ul>
    <ul>
    <p>文学相关</p>
    <ul>
        <p>唐宋诗词</p>
        <ul>
        <li>编辑唐宋诗词(待开发)</li>
        <li>新增唐宋诗词(待开发)</li>
        </ul>
    </ul>
    <ul>
        <p>毒鸡汤文案</p>
        <ul>
        <li>编辑毒鸡汤</li>
        <li>新增毒鸡汤</li>
        </ul>
    </ul>
    </ul>
    <ul>
    <p>个人计划</p>
    <ul>
        <li>新增个人近期计划</li>
        <li>修改个人近期计划</li>
        <li>完成个人近期计划</li>
    </ul>
    </ul>
</div>
</details>

<details>
<summary><b>2.交互管理</b></summary>
<div align="left">
    <ul>
    <p>评论管理</p>
    <ul>
    <li>查看评论</li>
    <li>删除评论(前台屏蔽)</li>
    </ul>
    </ul>
    <ul>
    <p>用户管理</p>
    <ul>
    <li>查看用户</li>
    <li>禁用用户(禁止登录)</li>
    <li>权限设置(管理员/用户)</li>
    </ul>
    </ul>
</div>
</details>

<details>
<summary><b>3.服务器管理</b></summary>
<div align="left">
    <ul>
    <p>服务器运行状态</p>
    <ul>
    <li>CPU占用比</li>
    <li>内存占用比</li>
    <li>网络收发占用</li>
    </ul>
    </ul>
    <ul>
    <p>运行日志</p>
    <ul>
    <li>nginx日志查看</li>
    <li>app错误日志查看</li>
    <li>nginx错误日志查看</li>
    </ul>
    </ul>
</div>
</details>

<details>
<summary><b>4.其他</b></summary>
<div align="left">
    <ul>
    <p>友链</p>
    <ul>
    <li>新增友链</li>
    <li>遗弃友链里程碑</li>
    </ul>
    </ul>
    <ul>
    <p>里程碑</p>
    <ul>
    <li>新增里程碑</li>
    <li>遗弃里程碑</li>
    </ul>
    </ul>
</div>
</details>


## 开始

### 依赖安装
* `U系Linux`、`Mac`用户可以通过根目录的`install.sh`脚本文件一键安装，如果出现错误也可以同Windows用户一样按照下面的步骤进行安装。
   ```bash
      cd Blogin
      ./install.sh
   ```


1. 安装MySQL
    进入MySQL或者mariaDB官网下载对应系统的安装包，进行安装即可。Linux用户可以通过命令进行安装
    
    ```shell script
    sudo apt-get install mysql
    ```
    
2. 安装redis

   进入redis官网下载安装包进行安装，Linux用户可以通过下面的命令安装

   ```shell script
   sudo apt-get install redis
   ```

   安装成功之后，通过如下命令开启redis服务

   ```shell script
   sudo service redis-server start
   ```

3. 创建数据库

   打开终端，输入如下命令进入MySQL控制台，具体命令根据你自己的MySQL数据库的设置而定

   ```shell script
   sudo mysql -u root -p
   ```

   ```mysql
   create database blog CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
   SHOW DATABASES ;
   ```

   如果控制台输出的内容中包含有`blog`数据库，则说明数据库创建成功了。
### 初始化

1. 克隆仓库代码

   进行这一步本地机器上必须先配置好git环境，具体细节请网上冲浪查询。

   ```shell script
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
   # gitee 第三方登录相关配置
   GITEE_CLIENT_ID='your gitee client id'
   GITEE_CLIENT_SECRET='your gitee client secret'
   ```

   **邮件服务器可以申请QQ邮箱或者163邮箱，具体申请流程请网上冲浪，十分简单，这里不做描述。**
   
   在项目根目录新建.flaskenv文件，在其中输入以下内容
   ```ini
   FLASK_APP=blogin
   FLASK_ENV=development
   ```
   指定当前环境为开发环境，指定当前APP为blogin.
   
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
     pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

5. 初始化数据库

   进入项目的根目录，使用如下命令进行数据库初始化

   ```bash
   cd Blogin
   # 初始化数据库以及相关配置
   flask initdb
   # 创建管理员账号
   flask admin
   ```

6. 运行

   ```bash
   flask run
   ```
   打开 http://127.0.0.1:5000 就可以看到页面了。

### Docker部署

首先确保在`.env` 文件中配置好了信息，通过下面的命令构建docker容器

```shell
sudo docker-compose up --build d
```

初始化数据库的表信息

```shell
# 初始化数据库迁移
sudo docker exec blogin /bin/bash -c "flask db init"
# 初始化数据库表
sudo docker exec blogin /bin/bash -c "flask initdb"
# 创建默认管理员账号
sudo docker exec blogin /bin/bash -c "flask admin-docker"
```

浏览器访问 http://127.0.0.1:8000 即可看到效果。


7. issue

   如果在运行过程中有任何问题出现，欢迎issue~
