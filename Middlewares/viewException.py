# -*- coding: utf-8 -*-
import time

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from Functions.api_msg import ProjMsg


def insert_log(msg):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('ERROR ' + current_time + str(msg) + '\n')
    with open('Logs/error_url.log', 'a') as f:
        f.write('ERROR ' + current_time + str(msg) + '\n')


class viewException(MiddlewareMixin):
    @staticmethod
    def process_exception(request, exception):
        info = f' {request.META["REMOTE_ADDR"]} {request.get_full_path()} ERROR: {exception}'
        insert_log(info)
        print(info)
        return JsonResponse({'code': '500', 'Msg': ProjMsg.SYS_ERROR.value, "data": info})
