# -*- coding: utf-8 -*-
from enum import Enum


class AppMsg(Enum):
    STOP_GENERATE_FAILED = "系统变量不存在, chat"
    SEND_MESSAGE_FAILED = "发送消息失败"
    SET_SYSTEM_MESSAGE_SUCCESS = "设置系统消息成功"
    MODIFY_PARAMS_SUCCESS = "修改参数成功"
    REGENERATE_MESSAGE_SUCCESS = "重新生成消息成功"
    MODIFY_MESSAGE_SUCCESS = "修改消息成功"
    STOP_GENERATE_SUCCESS = "停止生成成功"
    SEND_MESSAGE_SUCCESS = "发送消息成功"
    CLEAR_CONVERSATION_FAILED = "清空会话失败"
    CLEAR_CONVERSATION_SUCCESS = "清空会话成功"
    DELETE_CHAT_FAILED = "删除聊天失败"
    DELETE_CHAT_SUCCESS = "删除聊天成功"
    LOAD_HISTORY_SUCCESS = "加载历史成功"
    LOGIN_FAILED = "登录失败"
    CREATE_CHAT_FAILED = "创建聊天失败"
    CREATE_CHAT_SUCCESS = "创建聊天成功"
