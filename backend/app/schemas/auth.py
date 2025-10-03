from pydantic import BaseModel

class SignUpData(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class LoginData(BaseModel):
    email: str
    password: str