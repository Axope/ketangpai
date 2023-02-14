import json

import requests
import logging
from datetime import datetime
import time

sess = requests.session()
sess.headers = {
    'Host': 'openapiv5.ketangpai.com',
    'Referer': 'https://www.ketangpai.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'token': ''
}


def init_logging():
    t = datetime.now().strftime("%Y-%m-%d")
    f = open(f'log/{t}.log', 'w', encoding='utf-8')
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s,%(lineno)d]:%(message)s',
        stream=f
    )


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
    response = sess.post(
        url='https://openapiv5.ketangpai.com//UserApi/login',
        json=login_form
    )
    res = response.json()
    if res['status'] == 1:
        return res['data']['token']
    else:
        raise Exception(res['message'])


def get_course_list(semester: str, term: int) -> list:
    # 获取本学期课程列表
    response = sess.post(
        url='https://openapiv5.ketangpai.com//CourseApi/semesterCourseList',
        json={
            'isstudy': 1,
            'search': '',
            'semester': semester,
            'term': term
        }
    )
    res = response.json()
    if res['status'] == 1:
        return res['data']
    else:
        raise Exception(res['message'])


def get_homework(course_id: str) -> list:
    response = sess.post(
        url='https://openapiv5.ketangpai.com//FutureV2/CourseMeans/getCourseContent',
        json={
            'contenttype': 4,
            'courseid': course_id,
            'courserole': 0,
            'desc': 3,
            'dirid': 0,
            'lessonlink': [],
            'limit': 50,
            'page': 1,
            # 'reqtimestamp': 1676384885026,
            'sort': [],
            'vtr_type': ""
        }
    )
    res = response.json()
    if res['status'] == 1:
        return res['data']['list']
    else:
        raise Exception(res['message'])


def unix2localtime(ut) -> str:
    time_local = time.localtime(int(ut))
    return time.strftime("%Y-%m-%d %H:%M", time_local)


def output_homework(work: dict):
    print(f"作业名称: {work['title']} \t 作业截至时间: {unix2localtime(work['endtime'])}")


if __name__ == '__main__':
    init_logging()

    with open('config.json', 'r', encoding='utf-8') as fp:
        config = json.loads(fp.read())
        semester = config['semester']
        term = config['term']
        username = config['username']
        password = config['password']
        token = config['token']

    tk = login(username=username, password=password)
    sess.headers['token'] = tk
    # print(tk)
    course_list = get_course_list(semester=semester, term=term)
    # print(course_list)
    for course in course_list:
        course_name = course['coursename']
        course_id = course['id']
        homework_list = get_homework(course_id=course_id)
        # print(homework_list)
        # tmp_dict = {
        #     'course_name': course_name
        # }
        tmp_list = []
        for homework in homework_list:
            if homework['mstatus'] == 0:
                # tmp_dict[''] =
                tmp_list.append({
                    'title': homework['title'],
                    'endtime': homework['endtime']
                })
        if len(tmp_list) != 0:
            print(course_name, ':')
            for do_it in tmp_list:
                output_homework(do_it)

    # MDAwMDAwMDAwMLOGvd6Gqa9ohLVyoQ
# MDAwMDAwMDAwMLOGvd6Gqa9ohLVyoQ
# MDAwMDAwMDAwMLOGvd6GqatthLVyoQ
