from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import mapped_column
from model.BaseModel import Base
from datetime import datetime

class Book(Base):
    __tablename__ = 'book'
    __table_args__ = {"schema": "bookmazon"}
    book_id = mapped_column(String(13), primary_key=True)
    book_name = mapped_column(String(255), nullable=False)
    book_author = mapped_column(String(255))
    book_publisher = mapped_column(String(255))
    book_price = mapped_column(Integer, nullable=False)
    book_category = mapped_column(String(50))
    book_image_path = mapped_column(String(255))
    update_datetime = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now())
    create_datetime = mapped_column(DateTime, default=datetime.now())
