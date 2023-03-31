from django.shortcuts import render

from Functions import *
from .api_msg import AppMsg
from .models import UserInfo
from ChatGPT_WebAPI.settings import chat_assistant_interface_dict, websocket_interface_dict


# Create your views here.
def user_login(request):
    req_data = request_data(request, 'POST', ['username', 'password'])
    # 检查用户是否存在
    user_info = UserInfo.objects.filter(username=req_data['username'])
    if user_info:
        if user_info[0].password == encrypt(req_data['password']):
            # 刷新当前时间
            user_info.update(last_login=current_time())
            # 检查数据库中token是否存在
            if user_info[0].token:
                return api_response('200', AppMsg.LOGIN_SUCCESS.value, {'token': user_info[0].token})
            else:
                token = token_encrypt(req_data['username'] + req_data['password'])
                return api_response('200', AppMsg.LOGIN_SUCCESS.value, {'token': token})
        else:
            return api_response('400', AppMsg.LOGIN_FAILED.value)


def user_register(request):
    req_data = request_data(request, 'POST', ['username', 'password'])
    # 检查用户名是否已经存在
    if UserInfo.objects.filter(username=req_data['username']).exists():
        return api_response('400', AppMsg.USERNAME_EXISTS.value)
    # 创建新用户
    token = token_encrypt(req_data['username'] + req_data['password'])
    try:
        UserInfo.objects.create(
            username=req_data['username'],
            password=encrypt(req_data['password']),
            token=token
        )
        return api_response('200', AppMsg.REGISTER_SUCCESS.value, {'token': token})
    except Exception as e:
        return api_response('400', AppMsg.REGISTER_FAILED.value, {'error': str(e)})


def current_status(request):
    print(websocket_interface_dict.keys())
    print(chat_assistant_interface_dict.keys())
    return api_response('200', AppMsg.CURRENT_STATUS.value, {
        'websocket_interface': len(websocket_interface_dict),
        'chat_assistant_interface': len(chat_assistant_interface_dict)
    })
