from sqlalchemy.orm import declarative_base


class Base:
    __mapper_args__ = {"eager_defaults": True}

    @classmethod
    def from_pydantic(cls, model):
        return cls(**dict(model))


Base = declarative_base(cls=Base)
