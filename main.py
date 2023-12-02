from flask import Flask
from utils.dev_config import Config
from controller.UserController import userController
from controller.IndexController import indexController

import os
from datetime import timedelta
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

# 註冊藍圖
# app.register_blueprint(testController, url_prefix='/test')
app.register_blueprint(indexController, url_prefix='/')
app.register_blueprint(userController, url_prefix='/user')


# 啟動 Web Server
if __name__ == '__main__':
    app.run(port=Config.LISTENING_PORT, debug=True)