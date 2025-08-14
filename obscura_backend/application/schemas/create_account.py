from pydantic import BaseModel

class CreateAccountSchema(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str