from sqlalchemy.orm import scoped_session, sessionmaker

from utils.dev_config import Config
from sqlalchemy import create_engine

"""
    資料庫連線管理
"""


class DBConfig:
    def __init__(self):
        # db connection string
        db_url = f'postgresql://{Config.DB_ACCOUNT}:{Config.DB_PASSWORD}@{Config.DB_SEVER_HOST_NAME}:' \
                 f'{Config.DB_SEVER_HOST_PORT}/{Config.DB_NAME}'
        self.engine = create_engine(db_url, echo=True)
        # 確保資料庫連線獨立性
        session_factory = sessionmaker(self.engine)
        self.session = scoped_session(session_factory)


session = DBConfig().session
