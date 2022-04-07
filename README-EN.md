# Blogin

![python-depend.svg](https://7.dusays.com/2020/12/11/507ca007c94c0.svg)
![stars](https://img.shields.io/github/stars/weijiang1994/blogin)
![fork](https://img.shields.io/github/forks/weijiang1994/blogin)

Blogin is a personal blog website that base on flask development.

[中文文档](https://github.com/weijiang1994/Blogin/blob/master/README.md)

## Introduce

The personal blog site developed by the Flask Python Web framework consists of two parts: the front-end and the back-end.

### Front-end

1. **Personal Blog**
   - Support blog categorization
   - Support comment 
   - Support  share your blog to personal social network
   - Support blog archive
2. **Personal Gallery**
   - Support photo tag
   - Support comment and like
   - Support share your photo to personal social network
3. **Online Lite Tool**
   - Online word cloud graph generator
   - Online multi translation tool
   - Online Tang-Song poem search tool
   - Online ocr tool
   - Online IP real address search tool
4. **Comment System**
   - Support comment/delete/report
   - Support reply comment
5. **Personal Profile**
   - Personal profile card
   - Message notifycation
   - Modify your information
   - Record login log
6. **Tang-Song Poem**
   - Get a Tang-Song poem with random way
   - Get Song Ci with random way
   - Supply API to get Tang-Song poem
7. **Others**
   - Support make personal plan recently
   - Support the contribution heat map display for the past three months

### Back-end

1. **Content manage**

   - **Blog** 
     - Create blog
     - Modify blog
     - Delete blog(It's just masking the display on the front page, not actually deleting it from the database)
   - **Gallery**
     - Add photo
     - Modify Photo
     - Delete Photo(like blog)
   - **Literature**
     - Tang-Song poem
       - Modify(todo)
       - New(todo)
   - **Personal Plan**
     - Add a new personal plan
     - Modify personla plan
     - Finish personal plan

2. **Social Mange**

   - **Comment Manage**
     - Look up comments
     - Delete comment(like blog)
   - **User Manage**
     - Look up users
     - Ban user account

3. **Server Manage**

   - **Server Satus**
     - CPU Usage
     - Memory Usage
     - Network Status

   - **Log**
     - nginx Log
     - App Log
     - nginx error Log

4. **Others**

   - **Friend Link**
     - Add new friend link
     - Abandon a friend link
   - **Milestone**
     - Add new milestone
     - Abandon a milestone

## Start

### Dependencies

1. **Install mysql**

   Go to the official website of MySQL or mariaDB to download the installation package of the corresponding system and install it. Linux users can install via commands.

   ```shell
   sudo apt-get install mysql
   ```

2. **Install redis**

   Go to redis official website to download the installation package for installation. Linux users can install it by following the command.

   ```shell
   sudo apt-get install redis
   ```

   After successful installation, start the RedIS service with the following command.

   ```shell
   sudo service redis-server start
   ```

3. **Create Database**

   Open the terminal, enter the following command to enter the MySQL console, the specific command depends on your own MySQL database settings.

   ```shell
   sudo mysql -u root -p
   ```

   ```mysql
   create database blog CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
   SHOW DATABASES ;
   ```

   If the content of the console output contains the `blog` database, the database was created successfully.

### Initial

1. **Clone code**

   For this step, the git environment must be configured on the local machine first. Please surf the Internet for details.

   ```shell
   git clone https://github.com/weijiang1994/Blogin.git
   ```

2. **Configure environment variables** 

   Many properties in the project are private and confidential, so we can save the values of these properties in the `.env` file, and block the file when uploading the code. Create a new `.env` file in the root directory of the project, and enter the following in the file.

   ```INI
   MAIL_SERVER='your mail server'
   MAIL_USERNAME='your mail username'
   MAIL_PASSWORD='your mail server verify code' # not your email login password
   SECRET_KEY='your project secret'
   DATABASE_USER='your mysql/mariaDB database connect username'
   DATABASE_PWD='your mysql/mariaDB database connect user password'
   # BAIDU trans apiid and key
   BAIDU_TRANS_APPID='your app id for baidu trans'
   BAIDU_TRANS_KEY='your app key for baidu trans'
   # github oauth id and key
   GITHUB_CLIENT_ID='your github client id'
   GITHUB_CLIENT_SECRET='your github client secret'
   # gitee oauth id and key
   GITEE_CLIENT_ID='your gitee client id'
   GITEE_CLIENT_SECRET='your gitee client secret'
   ```

   **The mail server can apply for gmail mailbox or other mailbox. Please surf the Internet for the specific application process. It is very simple and will not be described here. **

   Create a new .flaskenv file in the project root directory and enter the following content

   ```ini
   FLASK_APP=blogin
   FLASK_ENV=development
   ```

3. **Create and activate the virtual environment**

   Because the dependencies of each project are different, Python provides a virtual environment tool to isolate the dependencies of each project. Use the following commands to create a virtual environment.

   ```shell
    cd Blogin
     python3 -m venv venv
   ```

   Activate it.

   ```shell
   source venv/bin/activate
   ```

   Activate it on Windows OS.

   ```shell
     venv\Scripts\activate
   ```

4. **Install python dependencies**

   After we enter the virtual environment, we can use the following command to install third-party dependencies.

   ```shell
     cd Blogin
     pip install -r requirements.txt -i https://pypi.douban.com/simple
   ```

5. **Init database**

   Enter the root directory of the project, use the following command to initialize the database.

   ```shell
   cd Blogin
   # init database and some configures
   flask initdb
   # create a admin account
   flask admin
   ```

6. **Run**

   ```shell
   flask run
   ```

   - Input http://127.0.0.1:5000 on your browser, then you can see the index page.
   - https://2dogz.cn online