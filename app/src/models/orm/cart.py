from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Boolean, text
from sqlalchemy.orm import relationship

from .base import Base


class CartOrm(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)
    session_id = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    is_placed = Column(Boolean, nullable=False, server_default=text("false"))

    cart_products = relationship("CartProductsOrm", backref="cart", lazy="immediate")


class CartProductsOrm(Base):
    __tablename__ = "cart_products"

    id = Column(Integer, primary_key=True)
    carts_id = Column(ForeignKey("carts.id"), nullable=False)
    product_id = Column(ForeignKey("products.id"), nullable=False)
    amount = Column(Integer, nullable=False, server_default=text("1"))

    product = relationship("ProductOrm", lazy="immediate")
