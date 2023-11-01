from flask import Flask
from utils.dev_config import Config
from controller.TestController import testController

app = Flask(__name__)
# 註冊藍圖
app.register_blueprint(testController, url_prefix='/test')

# 啟動 Web Server
if __name__ == '__main__':
    app.run(port=Config.LISTENING_PORT,debug=True)
