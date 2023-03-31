"""ChatGPT_WebAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
import APP_Users_Login.views
import APP_User_Operate.views

urlpatterns = [
    # ---------- APP_Users ---------- #
    path('api/user/register/', APP_Users_Login.views.user_register),  # 用户注册
    path('api/user/login/', APP_Users_Login.views.user_login),  # 用户登陆
    path('api/user/status/', APP_Users_Login.views.current_status),  # 用户登出

    # ---------- APP_Users_Operation ---------- #
    path('api/user/operation/new_chat/', APP_User_Operate.views.create_new_chat),
    path('api/user/operation/chat_list/', APP_User_Operate.views.load_history),
    path('api/user/operation/delete_chat/', APP_User_Operate.views.delete_chat),
    path('api/user/operation/clear_conversation/', APP_User_Operate.views.clear_conversation),
    path('api/user/operation/send_message/', APP_User_Operate.views.send_message),
    path('api/user/operation/stop_generate/', APP_User_Operate.views.stop_generate),
    path('api/user/operation/modify_message/', APP_User_Operate.views.modify_message),
    path('api/user/operation/set_system_message/', APP_User_Operate.views.set_system_message),
    path('api/user/operation/regenerate_message/', APP_User_Operate.views.regenerate_message),
    path('api/user/operation/modify_params/', APP_User_Operate.views.modify_params),
]
