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
