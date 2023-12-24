from datetime import datetime

from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import mapped_column

from model.BaseModel import Base


"""
    使用者資訊
"""
class User(Base):
    __tablename__ = 'user' # must write
    __table_args__ = {"schema": "bookmazon"}  # must write
    user_account = mapped_column(String(20), primary_key=True)
    user_password = mapped_column(Text)
    user_name = mapped_column(String(50))
    user_gender = mapped_column(String(1))
    user_identification = mapped_column(String(1))
    user_email = mapped_column(String(255))
    user_birthday = mapped_column(String(255))
    user_picture_path = mapped_column(String)
    update_datetime = mapped_column(DateTime, default=datetime.now())
    create_datetime = mapped_column(DateTime, default=datetime.now())


