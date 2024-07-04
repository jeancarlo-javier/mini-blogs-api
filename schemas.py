from pydantic import BaseModel, EmailStr, SecretStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: SecretStr

class PostCreate(BaseModel):
    title: str
    content: str
