import sqlalchemy
from sqlalchemy.orm import relationship

from app.db.models import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    username = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    balance = sqlalchemy.Column(sqlalchemy.Integer)
    cars = relationship('Car', lazy="noload")

