from typing import Type

from pydantic import BaseModel


class CustomResponse(BaseModel):
    message: str


default_response = CustomResponse(message="ok")
default_response_example = {
    200: {
        "description": "Default response",
        "content": {"application/json": {"example": {"message": "ok"}}},
    }
}


def response_model(model: Type["BaseModel"]) -> dict:
    """
    In case of inability to use constructor twice when providing response_model=<model>.

    Issue: `<https://github.com/tiangolo/fastapi/issues/3021>`_
    """
    # due to double init by fastapi if provide response_model = ShoppingCart
    return {200: {"model": model}}
