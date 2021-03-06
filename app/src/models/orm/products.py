from sqlalchemy import Column, Integer, Text, Float, Boolean

from .base import Base


class ProductOrm(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    price = Column(Float, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
