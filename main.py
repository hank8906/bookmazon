import os
from datetime import timedelta
from flask import Flask
from controller.CartController import cartController
from controller.ProductController import productController
from controller.UserController import userController
from controller.OrderController import orderController
from model.AuthUser import AuthUser
from utils.dev_config import Config
from flask_login import LoginManager
from model.User import User
from utils.dbUtil import session


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

# 註冊藍圖
app.register_blueprint(userController, url_prefix='/user')
app.register_blueprint(productController, url_prefix='/')
app.register_blueprint(cartController, url_prefix='/cart')
app.register_blueprint(orderController, url_prefix='/order')

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
    app.run(port=Config.LISTENING_PORT, debug=True)
