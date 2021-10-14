"""
# coding:utf-8
@Time    : 2020/10/19
@Author  : jiangwei
@File    : monitor
@Software: PyCharm
"""
import psutil
from blogin.emails import send_server_warning_mail
from blogin.extension import rd
import time
from threading import Thread


def monitor_server_status():
    while True:
        cpu_rate = psutil.cpu_percent()
        mem_rate = psutil.virtual_memory().percent

        if cpu_rate > 1 or mem_rate > 95:
            if not rd.get('warnEmail'):
                # send_server_warning_mail(cpu_rate=cpu_rate, mem_rate=mem_rate)
                rd.set('warnEmail', 1)
        time.sleep(5)
        print('start threading...')


def start_monitor_thread():
    th = Thread(target=monitor_server_status)
    th.start()
