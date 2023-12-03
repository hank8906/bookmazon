from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import mapped_column
from model.BaseModel import Base
from datetime import datetime

class CartItem(Base):
    __tablename__ = 'cart_item'
    __table_args__ = {"schema": "bookmazon"}
    cart_item_id = mapped_column(Integer, primary_key=True)
    cart_id = mapped_column(Integer,ForeignKey('bookmazon.cart.cart_id'))
    item_id = mapped_column(Integer,ForeignKey('bookmazon.item.item_id'))
    quantity = mapped_column(Integer)
    update_datetime = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now())
    create_datetime = mapped_column(DateTime, default=datetime.now())