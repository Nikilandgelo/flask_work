from sqlmodel import SQLModel, Field
from pydantic import field_serializer, field_validator
import re
import bcrypt


class AdvertisementSerializer(SQLModel):
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    owner_id: int = Field(foreign_key = "user.id", nullable=False)


class UserSerializer(SQLModel):
    name: str = Field(nullable=False, max_length=100)
    email: str = Field(unique=True)
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        if re.match(r'^\w+@\w+\.\w+$', value):
            return value
        else:
            raise ValueError('invalid email')
        

class UserCreateUpdateSerializer(UserSerializer):
    password: str = Field(nullable=False, min_length=8)
    
    @field_serializer('password')
    def hash_password(self, value: str, *args, **kwargs):
        salt = bcrypt.gensalt()
        hash_passwd = bcrypt.hashpw(value.encode(), salt)
        return hash_passwd.decode()