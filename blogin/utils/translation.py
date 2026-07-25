"""
# coding:utf-8
Translation service clients: Google, Baidu, Youdao.
"""
import hashlib
import http.client
import json
import random
import re
import urllib.parse
import urllib.request

import execjs
from flask import current_app

from blogin.setting import basedir


class GoogleTranslation:
    def __init__(self):
        self.url = 'https://translate.google.cn/translate_a/single'
        self.TKK = "434674.96463358"  # 随时都有可能需要更新的TKK值

        self.header = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": "NID=188=M1p_rBfweeI_Z02d1MOSQ5abYsPfZogDrFjKwIUbmAr584bc9GBZkfDwKQ80cQCQC34zwD4ZYHFMUf4F59aDQLSc79_LcmsAihnW0Rsb1MjlzLNElWihv-8KByeDBblR2V1kjTSC8KnVMe32PNSJBQbvBKvgl4CTfzvaIEgkqss",
            "referer": "https://translate.google.cn/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
            "x-client-data": "CJK2yQEIpLbJAQjEtskBCKmdygEIqKPKAQi5pcoBCLGnygEI4qjKAQjxqcoBCJetygEIza3KAQ==",
        }

        self.data = {
            "client": "webapp",
            "sl": "auto",
            "tl": "vi",
            "hl": "zh-CN",
            "dt": ["at", "bd", "ex", "ld", "md", "qca", "rw", "rm", "ss", "t"],
            "otf": "2",
            "ssel": "0",
            "tsel": "0",
            "kc": "1",
            "tk": "",
            "q": ""
        }

        with open(basedir + r'/res/token.js', 'r', encoding='utf-8') as f:
            self.js_fun = execjs.compile(f.read())

    def update_TKK(self):
        url = "https://translate.google.cn/"
        req = urllib.request.Request(url=url, headers=self.header)
        page_source = urllib.request.urlopen(req).read().decode("utf-8")
        self.TKK = re.findall(r"tkk:'([0-9]+\.[0-9]+)'", page_source)[0]

    def construct_url(self):
        base = self.url + '?'
        for key in self.data:
            if isinstance(self.data[key], list):
                base = base + "dt=" + "&dt=".join(self.data[key]) + "&"
            else:
                base = base + key + '=' + self.data[key] + '&'
        base = base[:-1]
        return base

    def query(self, q, lang_to=''):
        self.data['q'] = urllib.parse.quote(q)
        self.data['tk'] = self.js_fun.call('wo', q, self.TKK)
        self.data['tl'] = lang_to
        url = self.construct_url()
        req = urllib.request.Request(url=url, headers=self.header)
        response = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
        target_text = response[0][0][0]
        return target_text


class BaiduTranslation:
    def __init__(self, q, lang='en'):
        self.app_id = current_app.config.get('BAIDU_TRANS_APPID')
        self.key = current_app.config.get('BAIDU_TRANS_KEY')
        self.pre_url = '/api/trans/vip/translate'
        self.from_lang = 'auto'
        self.to_lang = lang
        self.http_client = None
        self.salt = random.randint(32768, 65536)
        sign = self.app_id + q + str(self.salt) + self.key
        sign = hashlib.md5(sign.encode()).hexdigest()
        self.url = self.pre_url + '?appid=' + self.app_id + '&q=' + urllib.parse.quote(
            q) + '&from=' + self.from_lang + '&to=' + self.to_lang + '&salt=' + str(
            self.salt) + '&sign=' + sign

    def query(self):
        try:
            self.http_client = http.client.HTTPConnection('api.fanyi.baidu.com')
            self.http_client.request('GET', self.url)
            response = self.http_client.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
            trans = result.get('trans_result')[0].get('dst')
            return trans
        except Exception:
            return False
        finally:
            if self.http_client:
                self.http_client.close()


class YoudaoTranslation:
    def __init__(self, q, from_lang='auto', to_lang='zh'):
        request_url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
        data = {'i': q,
                'from': from_lang,
                'to': to_lang,
                'smartresult': 'dict',
                'client': 'fanyideskweb',
                'salt': '15944508027607',
                'sign': '598c09b218f668874be4524f19e0be37',
                'ts': '1594450802760',
                'bv': '02a6ad4308a3443b3732d855273259bf',
                'doctype': 'json',
                'version': '2.1',
                'keyfrom': 'fanyi.web',
                'action': 'FY_BY_REALTlME',
                }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
        data = urllib.parse.urlencode(data)
        data = bytes(data, 'utf-8')
        req = urllib.request.Request(request_url, data, headers=headers)
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')
        html = json.loads(html)
        self.result = html['translateResult'][0][0]['tgt']

    def query(self):
        return self.result
