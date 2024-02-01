from typing import Optional

from pydantic import BaseModel, EmailStr, Field, PastDate


class ContactSchema(BaseModel):
    firstname: str = Field(min_length=4, max_length=20)
    lastname: str = Field(min_length=5, max_length=30)
    email: EmailStr
    phone: str = Field(min_length=3, max_length=13)
    bday: PastDate = None
    notes: Optional[str] = Field(max_length=250)


class ContactResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: str
    phone: str
    bday: PastDate
    notes: str
#    user_id: int

    class Config:
        from_attributes = True
