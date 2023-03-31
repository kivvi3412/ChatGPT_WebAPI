# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

from Functions import api_response
from Functions.api_msg import MWMsg
from APP_Users_Login.models import UserInfo

user_include_path = ["api/user/operation"]


# 用来验证用户是否有权限登陆的中间件
class UserAuthMiddleWare(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        url_path_req = request.get_full_path()
        token = request.POST.get('token')
        # 如果请求在列表内则需要验证用户是否登陆
        for url in user_include_path:
            if url in url_path_req:
                # 查询数据库中是否存在token
                user_token = UserInfo.objects.filter(token=token)
                if not user_token:  # 如果token不存在
                    return api_response('401', MWMsg.LOGIN_FAILED.value)
