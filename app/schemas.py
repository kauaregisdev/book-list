from pydantic import BaseModel

class TokenRequest(BaseModel):
    username: str
    password: str

class BookCreate(BaseModel):
    title: str
    author: str
    year: int

class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    user_id: int

    model_config = {
        'from_attributes': True
    }

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

    model_config = {
        'from_attributes': True
    }

class BookUpdate(BaseModel):
    title: str
    author: str
    year: int