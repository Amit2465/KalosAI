from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr
    username: str
    profile_photo: str

class UserCreate(UserBase):
    pass  

class UserOut(UserBase):
    id: str

    class Config:
        from_attributes = True

class UsernameUpdate(BaseModel):
    username: str