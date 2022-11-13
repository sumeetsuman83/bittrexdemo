from pydantic import BaseModel, Field, EmailStr


class UserSignupSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Sumeet Suman",
                "email": "sumeetsuman83@gmail.com",
                "password": "password@123"
            }
        }

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "sumeetsuman83@gmail.com",
                "password": "password@123"
            }
        }