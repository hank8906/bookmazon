import os
from datetime import timedelta

from cryptography.fernet import Fernet
from flask import Flask
from flask_login import LoginManager

from controller.CartController import cartController
from controller.ProductController import productController
from controller.UserController import userController
from model.AuthUser import AuthUser
from model.User import User
from utils.EmailUutil import init_email
from utils.config import params
from utils.dbUtil import session

# from controller.OrderController import orderController

app = Flask(__name__)
cipher_suite = Fernet(params['PRIVATE_KEY'])
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
app.config['MAIL_SERVER'] = params['MAIL_SERVER']
app.config['MAIL_PORT'] = params['MAIL_PORT']
app.config['MAIL_USE_SSL'] = eval(params['MAIL_USE_SSL'])
app.config['MAIL_USERNAME'] = params['MAIL_USERNAME']
decrypted_password = cipher_suite.decrypt(params['MAIL_PASSWORD'])
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
