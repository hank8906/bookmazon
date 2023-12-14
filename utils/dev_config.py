class Config:
    DB_ACCOUNT = 'app_001'
    DB_PASSWORD = 'app_001'
    DB_NAME = 'bookstore'
    DB_SEVER_HOST_NAME = 'localhost'
    DB_SEVER_HOST_PORT = '5432'
    LISTENING_PORT = 5001
    MAIL_SERVER = 'smtp.cc.ncu.edu.tw'  # 預設為 localhost
    MAIL_PORT = 25  # 預設為 25
    MAIL_USE_SSL = False  # 預設為 False
    MAIL_USERNAME = '111423059@cc.ncu.edu.tw'  # 預設為 None
    MAIL_PASSWORD = b'gAAAAABleb0Kl6Dkis6sAIRUA5nhPhrjW6f9D-SVGIvOwucSeEh1-Wep0dq_lNymqf6z5GVbRXSECjHz7YOzfyfkUcZDEMJD5A=='  # 預設為 None
    MAIL_DEFAULT_SENDER = MAIL_USERNAME  # 預設為 None，這個不設也可以
    PRIVATE_KEY = b'nwjZWj8-pjJ4bn3gebESwb2okum57VvzMBia5KwMaVA='
    RECEIVE_MAIL_USERNAME = '112423001@cc.ncu.edu.tw'  # 固定接收信件者