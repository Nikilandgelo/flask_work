from sqlmodel import Field, Relationship
from serializers import AdvertisementSerializer, UserCreateUpdateSerializer
from datetime import datetime
from sqlalchemy import func


class AutoId:
    id: int = Field(primary_key=True)


class Advertisement(AdvertisementSerializer, AutoId, table=True):
    __tablename__ = 'advertisement'

    created_at: datetime = Field(
        nullable=True,
        sa_column_kwargs = {'server_default': func.now()}
    )
    owner: list['User'] = Relationship(back_populates='adverts')


class User(UserCreateUpdateSerializer, AutoId, table=True):
    __tablename__ = 'user'
    
    adverts: Advertisement = Relationship(back_populates='owner')