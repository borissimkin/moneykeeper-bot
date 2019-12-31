import datetime

from sqlalchemy import Integer, Column, String, Date, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.db', echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    telegram_username = Column(String)
    telegram_user_id = Column(Integer, nullable=False, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    last_activity = Column(Date, default=datetime.datetime.now())
    date_registration = Column(Date, default=datetime.datetime.now())


class CategoryEarning(Base):
    __tablename__ = 'category_earning'

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)


class Earning(Base):
    __tablename__ = 'earning'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    category_id = Column(Integer, ForeignKey('category_earning.id'))


class CategoryConsumption(Base):
    __tablename__ = 'category_consumption'

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)


class Consumption(Base):
    __tablename__ = 'consumption'

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)


Base.metadata.create_all(engine)

