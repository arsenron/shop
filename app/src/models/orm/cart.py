from .base import Base
from sqlalchemy import (
    Column, Integer, Text, DateTime, ForeignKey, Boolean, text
)
from sqlalchemy.orm import relationship


class Carts(Base):
    __tablename__ = 'carts'

    id = Column(Text, primary_key=True)
    created_at = Column(DateTime, nullable=False, server_default=text("now()"))

    cart_products = relationship("CartProducts", backref="cart", lazy="immediate")


class CartProducts(Base):
    __tablename__ = 'cart_products'

    id = Column(Integer, primary_key=True)
    cart_id = Column(ForeignKey('carts.id'), nullable=False)
    product_id = Column(ForeignKey('products.id'), nullable=False)
    amount = Column(Integer, nullable=False, server_default=text("1"))
    is_placed = Column(Boolean, nullable=False, server_default=text("false"))

    product = relationship('Products', lazy="immediate")
