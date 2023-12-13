# 在 model 檔建立 PasswordResetToken 的 class
from datetime import datetime

from sqlalchemy import Integer
from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column

from model.BaseModel import Base


class PasswordResetToken(Base):
    __tablename__ = 'password_reset_tokens'
    __table_args__ = {"schema": "bookmazon"}
    id = mapped_column(Integer, primary_key=True)
    user_email = mapped_column(String(255), nullable=False)
    token = mapped_column(String(255), nullable=False)
    update_datetime = mapped_column(DateTime, default=datetime.now())
    create_datetime = mapped_column(DateTime, default=datetime.now())

