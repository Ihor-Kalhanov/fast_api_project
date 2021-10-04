from typing import List, Optional

from pydantic import PositiveInt

from app.apps import Base
from app.apps.cars.schemas import Car


class UserBase(Base):
    username: str
    email: Optional[str] = None
    balance: Optional[int] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: PositiveInt
    cars: Optional[List[Car]]

class Users(Base):
    users: Optional[List[User]]