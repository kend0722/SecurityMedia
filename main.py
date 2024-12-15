# -*- coding: utf-8 -*-
"""
@Time    : 2024/06/15 下午4:34
@Author  : Kend
@FileName: main.py.py
@Software: PyCharm
@modifier:
"""


# main.py
import argparse
from encryptor import encrypt_file, decrypt_file
from config import FILE_TYPE_VIDEO, FILE_TYPE_IMAGE, FILE_TYPE_LOG

def main():
    parser = argparse.ArgumentParser(description="Encrypt and decrypt files with hardware binding and time limit.")
    parser.add_argument('action', choices=['encrypt', 'decrypt'], help="Action to perform")
    parser.add_argument('input', help="Input file path")
    parser.add_argument('output', help="Output file path")
    parser.add_argument('--type', choices=['video', 'image', 'log'], default='video', help="Type of file (default: video)")
    parser.add_argument('--days', type=int, default=7, help="Expiration days (default: 7)")

    args = parser.parse_args()

    file_type_map = {
        'video': FILE_TYPE_VIDEO,
        'image': FILE_TYPE_IMAGE,
        'log': FILE_TYPE_LOG
    }

    file_type = file_type_map[args.type]

    if args.action == 'encrypt':
        print(f"Encrypting {args.input} to {args.output}...")
        encrypt_file(args.input, args.output, file_type, args.days)
        print("Encryption completed successfully.")
    elif args.action == 'decrypt':
        print(f"解密密文件 {args.input} to {args.output}...")
        file_type = decrypt_file(args.input, args.output)
        print(f"Decryption completed successfully. File type: {args.type}.")


if __name__ == "__main__":
    main()