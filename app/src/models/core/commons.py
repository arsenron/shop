from pydantic import BaseModel as PydanticBaseModel


class RoundedFloat(float):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return cls(round(v, 2))


class BaseModel(PydanticBaseModel):
    class Config:
        orm_mode = True