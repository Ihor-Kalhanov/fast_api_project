import sqlalchemy
from sqlalchemy import UniqueConstraint

from app.db.models import BaseModel


class Car(BaseModel):
    __tablename__ = 'car'

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    catalog_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("catalog.id"))
    __table_args__ = (UniqueConstraint("catalog_id", "name", name="car_id_name"),)
