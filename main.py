import os
from datetime import timedelta
from flask import Flask
from flask_mail import Mail

from controller.CartController import cartController
from controller.ProductController import productController
from controller.UserController import userController
from model.AuthUser import AuthUser
from utils.EmailUutil import init_email
from utils.dev_config import Config
from flask_login import LoginManager
from model.User import User
from utils.dbUtil import session
from cryptography.fernet import Fernet
# from controller.OrderController import orderController

app = Flask(__name__)
cipher_suite = Fernet(Config.PRIVATE_KEY)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
app.config['MAIL_SERVER'] = Config.MAIL_SERVER
app.config['MAIL_PORT'] = Config.MAIL_PORT
app.config['MAIL_USE_SSL'] = Config.MAIL_USE_SSL
app.config['MAIL_USERNAME'] = Config.MAIL_USERNAME
decrypted_password = cipher_suite.decrypt(Config.MAIL_PASSWORD)
app.config['MAIL_PASSWORD'] = decrypted_password.decode('utf-8')
init_email(app)
# 註冊藍圖
app.register_blueprint(userController, url_prefix='/user')
app.register_blueprint(productController, url_prefix='/')
app.register_blueprint(cartController, url_prefix='/cart')
# app.register_blueprint(orderController, url_prefix='/order')

# 初始化 Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


# login_manager.login_view = 'userController.login'
# 用戶加載函數
@login_manager.user_loader
def load_user(user_account):
    user = session.query(User).filter(User.user_account == user_account).first()
    if user is None:
        return
    auth_user = AuthUser(user=user)
    return auth_user


# 啟動 Web Server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=params['LISTENING_PORT'], debug=True)
