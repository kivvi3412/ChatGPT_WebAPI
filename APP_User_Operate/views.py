from APP_Users_Login.models import UserInfo
from .models import ChatInfo
from .api_msg import AppMsg
from Functions import *
from APP_Chat.utils import ChatAssistant
from ChatGPT_WebAPI.settings import chat_assistant_interface_dict


# Create your views here.
def create_new_chat(request):
    req_data = request_data(request, 'POST', ['token'])
    user_info = UserInfo.objects.filter(token=req_data['token'])
    # 获取用户ID, 新建chat_id
    default_info = {
        'user_id': user_info[0].user_id,
        'chat_id': uuid_generator(),
        'openai_params': {
            "temperature": 0.7,
            "max_tokens": 2048,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
        },
        'chat_summary': '',
        'chat_message': [{"role": "system", "content": ""}],
    }
    try:
        ChatInfo.objects.create(**default_info)
        return api_response('200', AppMsg.CREATE_CHAT_SUCCESS.value, {'chat_id': default_info['chat_id']})
    except Exception as e:
        return api_response('400', AppMsg.CREATE_CHAT_FAILED.value, {'error': str(e)})


def load_history(request):
    req_data = request_data(request, 'POST', ['token'])
    user_info = UserInfo.objects.filter(token=req_data['token'])
    chat_info = ChatInfo.objects.filter(user_id=user_info[0].user_id, is_deleted=False)
    return api_response('200', AppMsg.LOAD_HISTORY_SUCCESS.value, filter_obj_json(chat_info))


def delete_chat(request):
    req_data = request_data(request, 'POST', ['chat_id'])
    try:
        ChatInfo.objects.filter(chat_id=req_data['chat_id']).update(is_deleted=True)
        return api_response('200', AppMsg.DELETE_CHAT_SUCCESS.value)
    except Exception as e:
        return api_response('400', AppMsg.DELETE_CHAT_FAILED.value, {'error': str(e)})


def clear_conversation(request):
    req_data = request_data(request, 'POST', ['token'])
    try:
        user_id = UserInfo.objects.filter(token=req_data['token'])[0].user_id
        ChatInfo.objects.filter(user_id=user_id).update(is_deleted=True)
        return api_response('200', AppMsg.CLEAR_CONVERSATION_SUCCESS.value)
    except Exception as e:
        return api_response('400', AppMsg.CLEAR_CONVERSATION_FAILED.value, {'error': str(e)})


def send_message(request):
    req_data = request_data(request, 'POST', ['chat_id', 'message'])
    try:
        display_chat_summary_status = 0
        chat_assistant = ChatAssistant()
        # 保存chat_assistant对象
        chat_assistant_interface_dict[req_data['chat_id']] = chat_assistant
        # 从数据库中获取历史记录
        chat_info_db = ChatInfo.objects.filter(chat_id=req_data['chat_id'])[0]
        # 加载配置信息
        chat_assistant.modify_param(chat_info_db.openai_params)
        # 加载历史记录
        chat_assistant.load_history(eval(str(chat_info_db.chat_message)))
        # 生成新的消息
        response = chat_assistant.generate_response(req_data['message'], req_data['chat_id'])
        if "error" in response:
            return api_response('400', AppMsg.SEND_MESSAGE_FAILED.value, response)
        else:
            # 保存新的消息
            chat_info_db.chat_message = chat_assistant.messages
            # 查询数据库中摘要是否为空?
            if chat_info_db.chat_summary == '':
                display_chat_summary_status = 1
                chat_info_db.chat_summary = chat_assistant.summary
            # 保存新的摘要
            chat_info_db.save()
            return api_response('200', AppMsg.SEND_MESSAGE_SUCCESS.value, {
                'chat_summary': chat_info_db.chat_summary,
                'display': display_chat_summary_status,
                'user': req_data['message'],
                'assistant': chat_assistant.messages[-1]['content']
            })
    except Exception as e:
        return api_response('400', AppMsg.SEND_MESSAGE_FAILED.value, {'error': str(e), "msg": "系统错误或ws连接错误"})


def stop_generate(request):
    req_data = request_data(request, 'POST', ['chat_id'])
    # 从系统变量中找到chat_assistant对象并且执行pause
    try:
        chat_assistant_interface_dict[req_data['chat_id']].pause()
        return api_response('200', AppMsg.STOP_GENERATE_SUCCESS.value, {'message': 'stop'})
    except Exception as e:
        return api_response('400', AppMsg.STOP_GENERATE_FAILED.value, {'error': str(e)})


def modify_message(request):
    req_data = request_data(request, 'POST', ['chat_id', 'num', 'message'])
    try:
        chat_assistant = ChatAssistant()
        # 保存chat_assistant对象
        chat_assistant_interface_dict[req_data['chat_id']] = chat_assistant
        # 从数据库中获取历史记录
        chat_info_db = ChatInfo.objects.filter(chat_id=req_data['chat_id'])[0]
        # 加载配置信息
        chat_assistant.modify_param(chat_info_db.openai_params)
        # 加载历史记录
        chat_assistant.load_history(eval(str(chat_info_db.chat_message)))
        # 修改消息
        response = chat_assistant.modify_message(req_data['num'], req_data['chat_id'], req_data['message'])
        if "error" in response:
            return api_response('400', AppMsg.SEND_MESSAGE_FAILED.value, response)
        else:
            # 保存新的消息
            chat_info_db.chat_message = chat_assistant.messages
            chat_info_db.save()
            return api_response('200', AppMsg.REGENERATE_MESSAGE_SUCCESS.value, {
                'assistant': chat_assistant.messages[-1]['content']
            })
    except Exception as e:
        return api_response('400', AppMsg.SEND_MESSAGE_FAILED.value, {'error': str(e), "msg": "系统错误或ws连接错误"})


def set_system_message(request):
    req_data = request_data(request, 'POST', ['chat_id', 'message'])
    # 从数据库中找到这个对话并且修改
    chat_info_db = ChatInfo.objects.filter(chat_id=req_data['chat_id'])[0]
    chat_info_db.chat_message[0] = {"role": "system", "content": req_data['message']}
    chat_info_db.save()
    return api_response('200', AppMsg.SET_SYSTEM_MESSAGE_SUCCESS.value, {'message': req_data['message']})


def regenerate_message(request):
    try:
        req_data = request_data(request, 'POST', ['chat_id'])

        chat_assistant = ChatAssistant()
        # 保存chat_assistant对象
        chat_assistant_interface_dict[req_data['chat_id']] = chat_assistant
        # 从数据库中获取历史记录
        chat_info_db = ChatInfo.objects.filter(chat_id=req_data['chat_id'])[0]
        # 加载配置信息
        chat_assistant.modify_param(chat_info_db.openai_params)
        # 加载历史记录
        chat_assistant.load_history(eval(str(chat_info_db.chat_message)))
        # 重新生成消息
        response = chat_assistant.regenerate_response(req_data['chat_id'])
        if "error" in response:
            return api_response('400', AppMsg.SEND_MESSAGE_FAILED.value, response)
        else:
            # 保存新的消息
            chat_info_db.chat_message = chat_assistant.messages
            chat_info_db.save()
            return api_response('200', AppMsg.REGENERATE_MESSAGE_SUCCESS.value, {
                'assistant': chat_assistant.messages[-1]['content']
            })
    except Exception as e:
        return api_response('400', AppMsg.SEND_MESSAGE_FAILED.value, {'error': str(e), "msg": "系统错误或ws连接错误"})


def modify_params(request):
    req_data = request_data(request, 'POST', ['chat_id', 'params'])  # params输入json格式
    # 从数据库中找到这个对话并且修改
    chat_info_db = ChatInfo.objects.filter(chat_id=req_data['chat_id'])[0]
    chat_info_db.openai_params = eval(req_data['params'])
    chat_info_db.save()
    return api_response('200', AppMsg.MODIFY_PARAMS_SUCCESS.value, {'params': eval(req_data['params'])})
