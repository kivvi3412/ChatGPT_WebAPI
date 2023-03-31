# -*- coding: utf-8 -*-
from enum import Enum


class AppMsg(Enum):
    CURRENT_STATUS = "当前状态"
    USERNAME_EXISTS = "用户名已存在"
    ADDRESS_GET_SUCCESS = "获取地址成功"
    ADDRESS_DELETE_SUCCESS = "删除成功"
    ADDRESS_UPDATE_SUCCESS = "更新地址成功"
    ADDRESS_ID_NULL = "deliver_info_id不能为空"
    ADDRESS_MAX_NUMBER = "收货地址最多只能有10个"
    DEFAULT_ADDRESS_EXIST = "默认地址已存在"
    ADDRESS_ADD_SUCCESS = "添加地址成功"
    OPERATE_ERROR = "没有操作错误"
    USER_INEXISTENCE = "用户不存在"
    LOGIN_FAILED = "登录失败"
    LOGIN_SUCCESS = "登录成功"
    REGISTER_FAILED = "注册失败"
    REGISTER_SUCCESS = "注册成功"
    MODIFY_SUCCESS = "修改成功"
    CONTENT_NULL = "内容不能为空"
    INSPECT_SUCCESS = "查询成功"
    INSPECT_FAILED = "查询失败"
