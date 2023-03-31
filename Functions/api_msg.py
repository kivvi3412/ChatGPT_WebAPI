# -*- coding: utf-8 -*-
from enum import Enum


class ProjMsg(Enum):  # Project message
    SYS_ERROR = "Server internal error"


class MWMsg(Enum):  # Middleware message
    LOGIN_FAILED = "Login failed"
