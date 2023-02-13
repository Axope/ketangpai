import json

import requests
import logging
from datetime import datetime

base_url = 'https://openapiv5.ketangpai.com/'
sess = requests.session()
sess.headers = {
    'Host': 'openapiv5.ketangpai.com',
    'Referer': 'https://www.ketangpai.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'token': ''
}


def login(username: str, password: str) -> str:
    login_form = {
        'code': '',
        'email': username,
        'mobile': '',
        'password': password,
        'remember': '0',
        'type': 'login',
    }
    # 登录并获取token
    resp = sess.post(
        url=base_url + '/UserApi/login',
        json=login_form
    )
    res = resp.json()
    if res['status'] == 1:
        return res['data']['token']
    else:
        raise Exception(res['message'])


def init_logging():
    t = datetime.now().strftime("%Y-%m-%d")
    f = open(f'log/{t}.log', 'w', encoding='utf-8')
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s,%(lineno)d]:%(message)s',
        stream=f
    )


if __name__ == '__main__':
    init_logging()

    with open('config.json', 'r', encoding='utf-8') as fp:
        config = json.loads(fp.read())
        # semester = config['semester']
        # term = config['term']
        username = config['username']
        password = config['password']
        token = config['token']

    tk = login(username=username, password=password)
    sess.headers['token'] = tk
    print(tk)
