# -*- coding: utf-8 -*-
import uuid

from django.http import JsonResponse
from django.utils import timezone


def api_response(code, msg, data=None) -> JsonResponse:  # api返回
    """
    Convert data to json response.
    :param code: error code
    :param msg: show message
    :param data: data
    """
    if data is None:
        data = []
    return JsonResponse({'code': code, 'Msg': msg, 'data': data})


def token_encrypt(string: str) -> str:  # 加密token为唯一值
    """
    Encrypt string.
    :param string: input string
    """
    import hashlib
    import random
    sha1 = hashlib.sha1()
    sha1.update(string.encode('utf-8') + str(random.random()).encode('utf-8') + str(timezone.now()).encode('utf-8'))
    return sha1.hexdigest()


def encrypt(string: str) -> str:  # 加密为唯一值
    """
    Encrypt string.
    :param string: input string
    """
    import hashlib
    sha1 = hashlib.sha1()
    sha1.update(string.encode('utf-8') + str("##encrypt##").encode('utf-8'))
    return sha1.hexdigest()


def current_time(add_time=0) -> str:  # 获取当前时间
    """
    Get current time.
    param add_time: add time
    """
    return timezone.now() + timezone.timedelta(seconds=add_time)


def filter_obj_json(filter_obj, del_key: list = None) -> list:  # 将对象转换为json格式
    """
    Convert objects.filter object to json.
    :param filter_obj: table object
    :param del_key: delete key
    """
    if del_key is None:
        del_key = []
    temp_list = []
    for obj in filter_obj:
        obj = obj.__dict__
        if '_state' in obj:
            del obj['_state']
        for key in del_key:
            if key in obj:
                del obj[key]
        temp_list.append(obj)
    return temp_list


def request_data(request, method, need_key: list = None) -> dict:  # 获取请求数据
    """
    Get request data.
    :param request: request
    :param need_key: need key
    :param method: GET POST
    """
    if need_key is None:
        if method == 'GET':
            need_key = request.GET.keys()
        elif method == 'POST':
            need_key = request.POST.keys()
        else:
            return {"code": 400, "Msg": "Request method error."}
    data_dict = {}
    for key in need_key:
        if method == 'GET':
            get_key = str(request.GET.get(key))
            if get_key != '' and get_key != 'None':
                data_dict[key] = get_key
        elif method == 'POST':
            post_key = str(request.POST.get(key))
            if post_key != '' and post_key != 'None':
                data_dict[key] = post_key
        else:
            return {"code": 400, "Msg": "Request method error."}
    return data_dict


def uuid_generator() -> str:  # 生成uuid
    """
    Generate uuid.
    """
    return str(uuid.uuid4())


def pop_dict(dict_obj, key: list) -> dict:  # 删除字典中的某个key
    """
    Pop dict.
    :param dict_obj: dict
    :param key: key
    """
    new_dict_obj = dict_obj.copy()
    for k in key:
        if k in new_dict_obj:
            new_dict_obj.pop(k)
    return new_dict_obj


def replace_dict_element(dict_obj, replace_dict: dict) -> dict:  # 替换字典中的某个key
    """
    Replace dict element.
    :param dict_obj: dict
    :param replace_dict: replace dict
    """
    for k in replace_dict:
        if k in dict_obj:
            dict_obj[k] = replace_dict[k]
    return dict_obj


def inspect_element(dict_obj, key: list) -> list:  # 判断字典中是否有某个key
    """
    Inspect element.
    :param dict_obj: dict
    :param key: key
    """
    needed_element = []
    for element in key:
        if element not in dict_obj:
            needed_element.append(element)
    return needed_element
