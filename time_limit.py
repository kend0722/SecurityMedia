# -*- coding: utf-8 -*-
"""
@Time    : 2024/06/15 下午4:33
@Author  : Kend
@FileName: time_limit.py
@Software: PyCharm
@modifier:
"""


# time_limit.py
import time

def add_time_limit(timestamp, expiration_days):
    """计算文件的有效期"""
    expiration_time = timestamp + (expiration_days * 24 * 60 * 60)
    return expiration_time

def check_time_limit(timestamp, expiration_days):
    """检查文件是否在有效期内"""
    current_time = int(time.time())
    expiration_time = add_time_limit(timestamp, expiration_days)
    if current_time > expiration_time:
        raise ValueError("File has expired and cannot be decrypted.")