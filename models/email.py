from pydantic import BaseModel


class Email(BaseModel):
    receiver: str
    subject: str
    message: str
