from .base import Base
from sqlalchemy import (
    Column, Integer, Text, Float
)


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    price = Column(Float, nullable=False)
