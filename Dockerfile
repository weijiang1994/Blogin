# Use an official Python runtime as a parent image
FROM ubuntu:20.04

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

ENV TZ=Asia/Shanghai \
    DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8

# Install any needed packages specified in requirements.txt
RUN pwd \
    && sed -i 's@/archive.ubuntu.com/@/mirrors.huaweicloud.com/@g' /etc/apt/sources.list \
    && apt-get clean \
    && apt update \
    && apt-get install -y python3 gcc python3-dev python3-pip tzdata \
    && pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install gunicorn==20.0.4 cryptography -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Define environment variable
ENV NAME Blogin

# Run app.py when the container launches
CMD ["gunicorn", "wsgi:app", "-c", "gunicorn_conf.py"]