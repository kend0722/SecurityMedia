# -*- coding: utf-8 -*-
"""
@Time    : 2024/06/15 下午4:33
@Author  : Kend
@FileName: utils.py
@Software: PyCharm
@modifier:
"""


# utils.py
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import struct

def encrypt_data(data, key, iv):
    """加密数据"""
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=backend)
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(data) + encryptor.finalize()
    tag = encryptor.tag  # 获取 GCM 标签

    # 确保 tag 的长度是 16 字节
    assert len(tag) == 16, f"Tag length is {len(tag)}, expected 16 bytes"

    return ciphertext, tag

def decrypt_data(ciphertext, key, iv, tag):
    """解密数据"""
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=backend)
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_data