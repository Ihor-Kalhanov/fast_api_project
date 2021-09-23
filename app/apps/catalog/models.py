import sqlalchemy
from sqlalchemy.orm import relationship

from app.db.models import BaseModel



class Catalog(BaseModel):
    __tablename__ = 'catalog'

    title = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    cars = relationship('Car', lazy="noload")
