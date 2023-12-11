from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from model.BaseModel import Base
from datetime import datetime


class OrderItem(Base):
    __tablename__ = 'order_item'
    __table_args__ = {"schema": "bookmazon"}

    order_item_id = mapped_column(Integer, primary_key=True)
    order_id = mapped_column(Integer,ForeignKey('bookmazon.order.order_id'))
    item_id = mapped_column(Integer,ForeignKey('bookmazon.item.item_id'))
    quantity = mapped_column(Integer, nullable=False)
    update_datetime = mapped_column(DateTime, default=datetime.now())
    create_datetime = mapped_column(DateTime, default=datetime.now())