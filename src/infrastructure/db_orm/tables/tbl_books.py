from sqlalchemy import Column, Integer, String, Text, Date
from sqlalchemy_serializer import SerializerMixin

from src.infrastructure.db_orm.tables.base import Base


class TblBooks(Base, SerializerMixin):
    __tablename__ = 'tbl_books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(String(20), nullable=False, unique=True)
    name = Column(String(500), nullable=False, unique=True)
    author = Column(String(200), nullable=False)
    publisher = Column(String(500), nullable=False)
    release_date = Column(Date(), nullable=False)
    pages = Column(Integer(), nullable=False)
    description = Column(Text(), nullable=False)

    def __repr__(self):
        return str(self.to_dict())