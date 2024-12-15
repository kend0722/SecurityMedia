# -*- coding: utf-8 -*-
"""
@Time    : 2024/06/15 下午4:34
@Author  : Kend
@FileName: encryptor.py
@Software: PyCharm
@modifier:
"""


import os
import struct
import time

from config import FILE_HEADER_FORMAT, HEADER_SIZE, VERSION, ENCRYPTION_ALGORITHM_AES_GCM
from key_manager import generate_key_and_iv, generate_hardware_bound_key
from hardware_binding import get_hardware_id, verify_hardware_binding
from time_limit import add_time_limit, check_time_limit
from utils import encrypt_data, decrypt_data


def encrypt_file(input_path, output_path, file_type, expiration_days):
    """加密文件并添加硬件绑定和时间限制"""
    with open(input_path, 'rb') as f_in:
        data = f_in.read()

    # 获取硬件 ID 并生成硬件绑定的密钥
    hardware_id = get_hardware_id()
    hardware_bound_key = generate_hardware_bound_key(hardware_id)

    # 生成新的 IV
    iv = os.urandom(12)

    # 加密数据
    ciphertext, tag = encrypt_data(data, hardware_bound_key, iv)

    # 获取当前时间戳
    timestamp = int(time.time())

    # 打印调试信息
    print(f"版本号: {VERSION} (expected 4 bytes)")
    print(f"文件类型: {file_type} (expected 4 bytes)")
    print(f"加密算法: {ENCRYPTION_ALGORITHM_AES_GCM} (expected 4 bytes)")
    print(f"iv: {iv.hex()} (expected 12 bytes)")
    print(f"标签: {tag.hex()} (expected 16 bytes)")
    print(f"硬件绑定密钥: {hardware_bound_key.hex()} (expected 32 bytes)")
    print(f"时间戳: {timestamp} (expected 4 bytes)")

    # 构建文件头，包含版本号、文件类型、加密算法、IV、标签、硬件绑定的密钥和时间戳
    header = struct.pack(FILE_HEADER_FORMAT, VERSION, file_type, ENCRYPTION_ALGORITHM_AES_GCM, iv, tag, hardware_bound_key, timestamp)

    # 写入加密文件
    with open(output_path, 'wb') as f_out:
        f_out.write(header)
        f_out.write(ciphertext)



def decrypt_file(input_path, output_path):
    """解密文件并验证硬件绑定和时间限制"""
    with open(input_path, 'rb') as f_in:
        header = f_in.read(HEADER_SIZE)
        if len(header) != HEADER_SIZE:
            raise ValueError("无效的文件头")

        # 解包文件头
        version, file_type, encryption_algorithm, iv, tag, hardware_bound_key, timestamp = struct.unpack(FILE_HEADER_FORMAT, header)

        if version != VERSION or encryption_algorithm != ENCRYPTION_ALGORITHM_AES_GCM:
            raise ValueError("Unsupported file format or encryption algorithm")

        # 将 iv, tag, hardware_bound_key 转换为字节对象
        iv = bytes(iv)
        tag = bytes(tag)
        hardware_bound_key = bytes(hardware_bound_key)

        ciphertext = f_in.read()

    # 获取当前设备的硬件 ID 并生成硬件绑定的密钥
    current_hardware_id = get_hardware_id()
    current_key = generate_hardware_bound_key(current_hardware_id)

    # 打印调试信息
    print(f"Stored hardware_bound_key: {hardware_bound_key.hex()}")
    print(f"Current hardware_bound_key: {current_key.hex()}")

    # 验证硬件绑定的密钥是否匹配当前设备
    if not verify_hardware_binding(hardware_bound_key, current_key):
        raise ValueError("Hardware binding failed: This file can only be decrypted on the original device.")

    # 检查文件是否在有效期内
    check_time_limit(timestamp, expiration_days=7)  # 默认有效期为7天

    # 解密数据
    decrypted_data = decrypt_data(ciphertext, hardware_bound_key, iv, tag)

    # 写入解密后的文件
    with open(output_path, 'wb') as f_out:
        f_out.write(decrypted_data)

    return file_type

