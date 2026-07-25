"""
# coding:utf-8
IP address lookup utilities.
"""
import json
import requests

from blogin.utils.constants import IP_QUERY, LANGUAGE


def get_ip_real_add(ip):
    if ip == '127.0.0.1':
        return '本地IP'
    response = requests.get(IP_QUERY.format(ip))
    response = response.text
    response = json.loads(response)
    if response['status'] == 'fail':
        return '定位失败'
    return response['country'] + '-' + response['city']


class IPQuery:
    def __init__(self, ip, lang='zh-CN'):
        self.ip = ip.strip()
        self.lang = LANGUAGE.get(lang)
        self.url = ("http://ip-api.com/json/{}?lang={}&fields=status,continent,continentCode,isp,zip,message,"
                    "timezone,country,region,regionName,city,lat,lon,query")

    def query(self):
        if self.ip == '127.0.0.1':
            return '本地IP'
        response = requests.get(self.url.format(self.ip, self.lang))
        response = response.text
        response = json.loads(response)
        if response['status'] == 'fail':
            return '查询失败'
        return [response['country'], response['regionName'], response['city'], response['continent'],
                response['continentCode'], response['isp'], response['timezone'], response['lat'], response['lon']]
