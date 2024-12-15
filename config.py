# -*- coding: utf-8 -*-
"""
@Time    : 2024/06/15 下午4:31
@Author  : Kend
@FileName: config.py.py
@Software: PyCharm
@modifier:
"""

import struct

# 版本号、文件类型和加密算法的常量
VERSION = 1
FILE_TYPE_VIDEO = 1
FILE_TYPE_IMAGE = 2
FILE_TYPE_LOG = 3
ENCRYPTION_ALGORITHM_AES_GCM = 1


# 文件头结构
FILE_HEADER_FORMAT = '<III12s16s32sI'  # 版本号, 文件类型, 加密算法, IV, 标签, 密钥, 时间戳
HEADER_SIZE = struct.calcsize(FILE_HEADER_FORMAT)

print(f"FILE_HEADER_FORMAT: {FILE_HEADER_FORMAT}")