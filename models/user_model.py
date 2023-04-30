from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class UserModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="userId")
    email: str = Field(..., example="johndoe@example.com")
    phone: str = Field(..., example="1234567890")
    name: str = Field(..., example="John Doe")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.utcnow, alias="updatedAt")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "johndoe@example.com",
                "phone": "1234567890",
                "name": "John Doe"
            }
        }

class UserUpdate(BaseModel):
    email: Optional[str]
    phone: Optional[str]
    name: Optional[str]

    class Config:
        schema_extra = {
             "example": {
                "email": "johndoe@example.com",
                "phone": "1234567890",
                "name": "John Doe"
            }
        }