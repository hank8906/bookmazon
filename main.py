from flask import Flask
from utils.dev_config import Config
from controller.UserController import userController
from controller.IndexController import indexController
from controller.CartController import cartController
from controller.TestController import testController
from controller.ProductController import productController
# from controller.OrderController import orderController

import os
from datetime import timedelta
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

# 註冊藍圖
# app.register_blueprint(testController, url_prefix='/test')
# app.register_blueprint(indexController, url_prefix='/')
app.register_blueprint(userController, url_prefix='/user')
app.register_blueprint(productController, url_prefix='/')
app.register_blueprint(cartController, url_prefix='/cart')
# app.register_blueprint(orderController, url_prefix='/order')

# 這坨login manager的東西我不知道要放哪(´_ゝ`)
from flask_login import LoginManager
from model.User import User
from utils.dbUtil import session
# 初始化 Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'userController.login'
# 用戶加載函數
@login_manager.user_loader
def load_user(user_account):
    user = session.query(User).filter(User.user_account == user_account).first()
    return user


# 啟動 Web Server
if __name__ == '__main__':
    app.run(port=Config.LISTENING_PORT, debug=True)

