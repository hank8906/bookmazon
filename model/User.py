from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column
from model.BaseModel import Base
from datetime import datetime

"""
    使用者資訊
"""
class User(Base):
    __tablename__ = 'user'
    __table_args__ = {"schema": "bookmazon"}
    user_account = mapped_column(String(20), primary_key=True)
    user_password = mapped_column(String(16))
    user_identification = mapped_column(String(1))
    user_email = mapped_column(String(255))
    user_birthday = mapped_column(String(255))
    update_datetime = mapped_column(DateTime, default=datetime.now())
    create_datetime = mapped_column(DateTime, default=datetime.now())
