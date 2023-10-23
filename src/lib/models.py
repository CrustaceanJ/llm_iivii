from pydantic import BaseModel


class InputMessage(BaseModel):
    message: str
    user_id: str


class ResponseMessage(BaseModel):
    answer: str
