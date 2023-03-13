# !/usr/bin/python3.10
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


# 获取本学期课程列表
def get_course_list(semester: str, term: int) -> list:
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
            'sort': [],
            'vtr_type': ""
        }
    )
    res = response.json()
    if res['status'] == 1:
        return res['data']['list']
    else:
        raise Exception(res['message'])


def get_test(course_id: str) -> list:
    response = sess.post(
        url='https://openapiv5.ketangpai.com//FutureV2/CourseMeans/getCourseContent',
        json={
            'contenttype': 6,
            'courseid': course_id,
            'courserole': 0,
            'desc': 3,
            'dirid': 0,
            'lessonlink': [],
            'limit': 50,
            'page': 1,
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
    # print(type(ut), ut)
    if ut == "0":
        return "不限"
    time_local = time.localtime(int(ut))
    return time.strftime("%Y-%m-%d %H:%M", time_local)


def output_homework(work: dict):
    print(f"作业名称: {work['title']} \t 作业截至时间: {unix2localtime(work['endtime'])}")


def output_test(work: dict):
    print(f"测试名称: {work['title']} \t 测试截至时间: {unix2localtime(work['endtime'])}")


#  打印未完成的作业
def out_undo_homework(course_list: list):
    f = 0
    for course in course_list:
        course_name = course['coursename']
        course_id = course['id']
        homework_list = get_homework(course_id=course_id)
        tmp_list = []
        for homework in homework_list:
            if homework['mstatus'] == 0:
                tmp_list.append({
                    'title': homework['title'],
                    'endtime': homework['endtime']
                })
        if len(tmp_list) != 0:
            f = 1
            print(course_name, '未完成作业:')
            for do_it in tmp_list:
                output_homework(do_it)
    if f == 0:
        print('作业已全部完成')


#  打印未完成的测试
def out_undo_test(course_list: list):
    f = 0
    for course in course_list:
        course_name = course['coursename']
        course_id = course['id']
        test_list = get_test(course_id=course_id)
        tmp_list = []
        for test in test_list:
            if test['submit_state'] <= 2:
                # print("DE#", test['over'])
                tmp_list.append({
                    'title': test['title'],
                    'endtime': test['endtime']
                })
        if len(tmp_list) != 0:
            f = 1
            print(course_name, '未完成测试:')
            for do_it in tmp_list:
                output_test(do_it)
    if f == 0:
        print('测试已全部完成')


if __name__ == '__main__':
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
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    course_list = get_course_list(semester=semester, term=term)
    out_undo_homework(course_list)
    out_undo_test(course_list)
