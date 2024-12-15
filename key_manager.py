# -*- coding: utf-8 -*-
"""
@Time    : 2024/06/15 下午4:32
@Author  : Kend
@FileName: key_manager.py
@Software: PyCharm
@modifier:为了确保在同一台设备上生成的 hardware_bound_key 是一致的，我们需要移除 os.urandom(32)，
并使用一个固定的密钥或基于硬件 ID 生成的密钥。我们可以使用 PBKDF2HMAC 来从硬件 ID 中派生出一个稳定的密钥，而不是每次都生成随机密钥。
"""

import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
def generate_key_and_iv():
    """生成随机密钥和IV"""
    key = os.urandom(32)  # 256-bit key for AES-256
    iv = os.urandom(12)   # 96-bit IV for GCM
    return key, iv

def generate_hardware_bound_key(hardware_id):
    """生成硬件绑定的密钥"""
    # 使用硬件 ID 作为 salt，派生出一个稳定的密钥
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=hardware_id,
        iterations=100000,
        backend=default_backend()
    )
    # 使用固定字符串作为输入密钥材料 (IKM)，确保每次生成相同的密钥
    fixed_key_material = b"fixed-key-material-for-hardware-binding"
    hardware_bound_key = kdf.derive(fixed_key_material)
    return hardware_bound_key
