# Use an official Python runtime as a parent image
FROM ubuntu:20.04

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pwd \
    && sed -i 's@/archive.ubuntu.com/@/mirrors.huaweicloud.com/@g' /etc/apt/sources.list \
    && apt-get clean \
    && apt update \
    && apt-get install -y python3 gcc python3-dev python3-pip \
    && pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install gunicorn==20.0.4 cryptography -i https://pypi.tuna.tsinghua.edu.cn/simple

# Define environment variable
ENV NAME Blogin

# Run app.py when the container launches
CMD ["gunicorn", "wsgi:app", "-b", "0.0.0.0:8000", "-k", "eventlet", "-w", "4", "--worker-connections", "1000", "--timeout", "60", "--graceful-timeout", "60", "--error-logfile", "/var/logs/blogin_error.log", "--access-logfile", "/var/logs/blogin_access.log", "--log-level", "info"]