# -*- coding: utf-8 -*-
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer

from ChatGPT_WebAPI.settings import websocket_interface_dict, chat_assistant_interface_dict


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.chat_id = None

    def websocket_connect(self, message):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.accept()  # 允许链接
        websocket_interface_dict[self.chat_id] = self

    def websocket_receive(self, message):
        print('chat_id:', self.chat_id)
        print('message:', message)

    def websocket_disconnect(self, message):
        print('chat_id:', self.chat_id)
        print('message:', 'disconnect')
        if self.chat_id in websocket_interface_dict:
            websocket_interface_dict.pop(self.chat_id)
        if self.chat_id in chat_assistant_interface_dict:
            chat_assistant_interface_dict.pop(self.chat_id)
        raise StopConsumer()
