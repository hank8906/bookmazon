import os
from dotenv import dotenv_values

# 取得專案根目錄的絕對路徑
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 根據 FLASK_ENV 取得相對應的環境變數檔案
environment = os.environ.get('FLASK_ENV', 'development')

params = []
if environment == 'test':
    env_file_path = os.path.join(project_root, ".test.env")
    params = dotenv_values(env_file_path)
elif environment == 'prod':
    env_file_path = os.path.join(project_root, ".prod.env")
    params = dotenv_values(env_file_path)
elif environment == 'dev':
    env_file_path = os.path.join(project_root, ".dev.env")
    params = dotenv_values(env_file_path)
else:
    env_file_path = os.path.join(project_root, ".dev.env")
    params = dotenv_values(env_file_path)
