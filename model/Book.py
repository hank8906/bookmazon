from sqlalchemy import String, DateTime, Numeric
from sqlalchemy.orm import mapped_column, relationship
from model.BaseModel import Base
from datetime import datetime

"""
書籍資訊

"""

class Book(Base):
    __tablename__ = 'book'
    __table_args__ = {"schema": "bookmazon"}
    book_id = mapped_column(String(13), primary_key=True)
    book_name = mapped_column(String(255))
    book_author = mapped_column(String(255))
    book_publisher = mapped_column(String(255))
    book_price = mapped_column(Numeric(10, 2))
    book_category = mapped_column(String(50))
    book_image_path = mapped_column(String(255))
    update_datetime = mapped_column(DateTime, default=datetime.now())
    create_datetime = mapped_column(DateTime, default=datetime.now())
    item = relationship("Item", foreign_keys=[book_id], primaryjoin="Book.book_id==Item.book_id")

