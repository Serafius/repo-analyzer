from pydantic import BaseModel


class ResponseModel(BaseModel):
    data: dict | list | str | None
    isSuccess: bool
    error: str | None
    status: str | int | None
