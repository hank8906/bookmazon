from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from utils.config import params

"""
    資料庫連線管理
"""

class DBConfig:
    def __init__(self):
        DB_ACCOUNT = params['DB_ACCOUNT']
        DB_PASSWORD = params['DB_PASSWORD']
        DB_SEVER_HOST_NAME = params['DB_SEVER_HOST_NAME']
        DB_SEVER_HOST_PORT = params['DB_SEVER_HOST_PORT']
        DB_NAME = params['DB_NAME']

        # db connection string
        db_url = f'postgresql://{DB_ACCOUNT}:{DB_PASSWORD}@{DB_SEVER_HOST_NAME}:' \
                 f'{DB_SEVER_HOST_PORT}/{DB_NAME}'
        self.engine = create_engine(db_url, echo=True)
        # 確保資料庫連線獨立性
        session_factory = sessionmaker(self.engine)
        self.session = scoped_session(session_factory)

session = DBConfig().session
