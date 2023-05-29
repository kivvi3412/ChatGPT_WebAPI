# -*- coding: utf-8 -*-
import openai

from ChatGPT_WebAPI.settings import websocket_interface_dict
from ChatGPT_WebAPI.settings import openai_api


class ChatAssistant(object):
    def __init__(self):
        self.api_key = openai_api
        self.summary = ""  # 摘要
        self.model = "gpt-3.5-turbo"
        self.messages = [{"role": "system", "content": ""}]
        self.paused = False
        self.openai_params = {
            "temperature": 0.7,
            "max_tokens": 2048,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }

    @staticmethod
    def get_token_count(messages):
        return int(len(str(messages)) * 0.95)

    def set_api_key(self, api_key: str):
        self.api_key = api_key

    def load_history(self, history: list):
        """Loads a list of messages into the chat assistant."""
        self.messages = history.copy()

    def add_message(self, role: str, content: str):  # 一般用于添加系统的消息, 用户的消息用generate_response
        """
        自动添加消息到messages和current_messages
        """
        # 2048 is the max number of tokens for a single message
        if role == "user" and self.get_token_count([{"role": role, "content": content}]) > 2048:
            return False
        self.messages.append({"role": role, "content": content})
        return True

    def generate_summary(self):
        user_messages = [msg['content'] for msg in self.messages if msg['role'] == 'user']
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                temperature=0,
                max_tokens=10,
                api_key=self.api_key,
                messages=[
                    {"role": "system", "content": "Summarize the conversation"},
                    {"role": "user", "content": user_messages[0]},
                ]
            )
            self.summary = response.choices[0].message.content
            return self.summary
        except Exception as e:
            return {"error": str(e)}

    def generate_response(self, user_input: str, chat_id: str):
        self.add_message("user", user_input)
        temp_messages = self.messages.copy()  # 用于计算token数量
        while self.get_token_count(temp_messages) > 4096:  # 4096是单次请求的最大token数量
            temp_messages.pop(1)  # 不删除系统消息
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                temperature=self.openai_params["temperature"],
                max_tokens=self.openai_params["max_tokens"],
                top_p=self.openai_params["top_p"],
                frequency_penalty=self.openai_params["frequency_penalty"],
                presence_penalty=self.openai_params["presence_penalty"],
                messages=temp_messages,
                api_key=self.api_key,
                stream=True,
            )
        except Exception as e:
            return {"error": str(e)}

        # 如果count(role:user) = 1 说明是第一次回复, 需要加入摘要
        if len([msg for msg in self.messages if msg['role'] == 'user']) == 1:
            self.generate_summary()

        # 进行流式输出
        self.paused = False
        temp_assistant_output = ""
        if chat_id in websocket_interface_dict:
            for msg in response:
                if 'content' in dict(msg["choices"][0]["delta"]):
                    msg_part = msg["choices"][0]["delta"]["content"]
                    temp_assistant_output += msg_part
                    print(msg_part, end="")
                    websocket_interface_dict[chat_id].send(msg_part)
                if self.paused:  # 如过用户终止本次对话, 则不再继续输出
                    break

            self.add_message("assistant", temp_assistant_output)
            return {"success": str(temp_assistant_output)}
        else:
            return {"error": "The user did not make a websocket connection"}

    def pause(self):  # 对本次对话进行中断
        self.paused = True

    def set_system_message(self, content: str):
        self.messages[0]['content'] = content

    def regenerate_response(self, chat_id: str):
        # 删除messages中的的最后一条消息
        self.messages.pop()
        last_message = self.messages[-1]
        self.messages.pop()
        # 重新生成回复
        return self.generate_response(last_message['content'], chat_id)

    def modify_message(self, index: int, chat_id: str, new_content: str):
        # Check if the new content is too long
        if self.get_token_count(new_content) > 2048:
            return False

        # Remove all messages after the modified one
        self.messages = self.messages[:int(index)]

        # Add the modified message
        return self.generate_response(new_content, chat_id)

    def modify_param(self, param_dict: dict):
        self.openai_params.update(param_dict)
