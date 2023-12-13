from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import mapped_column, relationship, foreign
from model.BaseModel import Base
from datetime import datetime

class OrderItem(Base):
    __tablename__ = 'order_item'
    __table_args__ = {"schema": "bookmazon"}
    order_item_id = mapped_column(Integer, primary_key=True)
    order_id = mapped_column(Integer, nullable=False)
    item_id = mapped_column(Integer, nullable=False)
    quantity = mapped_column(Integer, nullable=False)
    update_datetime = mapped_column(DateTime, default=datetime.now())
    create_datetime = mapped_column(DateTime, default=datetime.now())
    order = relationship("Order", back_populates="items", foreign_keys=[order_id])