# -*- coding: utf-8 -*-
"""
@Time    : 2024/06/15 下午4:32
@Author  : Kend
@FileName: hardware_binding.py
@Software: PyCharm
@modifier:
"""

import platform
import uuid
import hashlib
import subprocess


def get_hardware_id():
    """获取硬件标识信息"""
    try:
        # 获取主板序列号
        motherboard_serial = subprocess.check_output('wmic baseboard get serialnumber').decode().strip().split('\n')[
            1].strip()

        # 获取硬盘序列号
        disk_serial = subprocess.check_output('wmic diskdrive get serialnumber').decode().strip().split('\n')[1].strip()

        # 获取 MAC 地址
        mac_address = ':'.join(
            ['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 2)][::-1])

        # 将硬件标识信息组合成字符串
        hardware_info = f"{motherboard_serial}{disk_serial}{mac_address}"

        # 使用 SHA-256 哈希硬件标识信息，生成固定长度的硬件 ID
        hardware_id = hashlib.sha256(hardware_info.encode()).digest()

        print(f"硬件-ID: {hardware_id.hex()}")

        return hardware_id
    except Exception as e:
        raise RuntimeError(f"获取硬件标识信息失败: {e}")


def verify_hardware_binding(stored_key, current_key):
    """验证硬件绑定的密钥是否匹配"""
    return stored_key == current_key
