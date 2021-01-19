# 监听本地端口
bind = '127.0.0.1:8000'
# 工作进程数
workers = 3
# 代码修改自动重新加载
reload = True
# 工作模式
worker_class = 'eventlet'
# 打印全部配置
print_config = True
# 日志配置
loglevel = 'info'
accesslog = '/home/jiangwei/log/gunicorn_acess.log'
errorlog = '/home/jiangwei/log/gunicorn_error.log'
pidfile = '/home/jiangwei/log/gunicorn.pid'
# 最大并发量
worker_connections = 2000
# 守护进程
daemon = False
