from sqlalchemy.orm import declarative_base


class Base:
    __mapper_args__ = {"eager_defaults": True}


Base = declarative_base(cls=Base)
