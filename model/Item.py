from sqlalchemy import String, DateTime, Integer, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import mapped_column, relationship
from model.BaseModel import Base
from datetime import datetime

"""
item資訊

"""

class Item(Base):
    __tablename__ = 'item'
    __table_args__ = {"schema": "bookmazon"}
    item_id = mapped_column(Integer, primary_key=True)
    book_id = mapped_column(String(13))
    item_status = mapped_column(String(1))
    book_count = mapped_column(Integer)
    provider_account = mapped_column(String(20))
    update_datetime = mapped_column(DateTime, default=datetime.now())
    create_datetime = mapped_column(DateTime, default=datetime.now())
