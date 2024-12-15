SecurityMedia/
│
├── main.py                  # 主程序入口
├── encryptor.py            # 加密和解密逻辑
├── key_manager.py          # 密钥管理
├── hardware_binding.py     # 硬件绑定逻辑
├── time_limit.py           # 时间限制逻辑
├── utils.py                # 辅助工具函数
└── config.py               # 配置文件

密钥管理：如果你需要在不同设备上解密文件，可以考虑使用公钥/私钥对或证书来进行身份验证，而不是依赖硬件绑定。
