from sqlalchemy import String, DateTime, Integer, ForeignKey, func
from sqlalchemy.orm import mapped_column
from model.BaseModel import Base
from datetime import datetime

class Cart(Base):
    __tablename__ = 'cart'
    __table_args__ = {"schema": "bookmazon"}
    cart_id = mapped_column(Integer, primary_key=True)
    user_account = mapped_column(String(20), ForeignKey('bookmazon.user.user_account'))
    update_datetime = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now())
    create_datetime = mapped_column(DateTime, default=datetime.now())