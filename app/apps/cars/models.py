import sqlalchemy

from app.db.models import BaseModel


class Car(BaseModel):
    __tablename__ = 'car'
    __table_args__ = {'extend_existing': True}

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    amount = sqlalchemy.Column(sqlalchemy.Integer, default=0, )
    catalog_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("catalog.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
