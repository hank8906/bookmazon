from sqlalchemy import Integer, String, Numeric, DateTime
from sqlalchemy.orm import mapped_column, relationship
from model.BaseModel import Base
from datetime import datetime

class Order(Base):
    __tablename__ = 'order'
    __table_args__ = {"schema": "bookmazon"}
    order_id = mapped_column(Integer, primary_key=True)
    user_account = mapped_column(String(20), nullable=False)
    order_total_price = mapped_column(Numeric(10, 2))
    order_status = mapped_column(String(1))
    update_datetime = mapped_column(DateTime, default=datetime.now())
    create_datetime = mapped_column(DateTime, default=datetime.now())
    items = relationship("OrderItem", back_populates="order")