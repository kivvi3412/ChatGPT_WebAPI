# -*- coding: utf-8 -*-
import time

from django.utils.deprecation import MiddlewareMixin


def insert_log(msg):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    with open('Logs/access_url.log', 'a') as f:
        f.write('INFO ' + current_time + str(msg) + '\n')


class RequestLogMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        post_data = None
        if request.method == 'POST':  # 获得post 请求内容
            post_data = dict(request.POST)
        insert_log(
            f' {request.META["REMOTE_ADDR"]} "{request.method}" PATH: "{request.get_full_path()}" POST_DATA: "{post_data}" "{request.META["HTTP_USER_AGENT"]}"')
