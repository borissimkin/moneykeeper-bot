import datetime
from contextlib import contextmanager

from sqlalchemy import Integer, Column, String, ForeignKey, create_engine, Float, DateTime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:///database.db', echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    telegram_username = Column(String)
    telegram_user_id = Column(Integer, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    last_activity = Column(DateTime, default=datetime.datetime.now())
    date_registration = Column(DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return f"<User ('{self.id}', '{self.telegram_username}', '{self.telegram_user_id}', " \
            f"'{self.first_name}', '{self.last_name}', '{self.last_activity}', '{self.date_registration}')>"

    def __eq__(self, other):
        return isinstance(other, User) and other.id == self.id

    def update_activity(self, session, now):
        self.last_activity = now
        session.commit()

    def update_username(self, session, username):
        if username != self.telegram_username:
            self.telegram_username = username
            session.commit()

    def get_username(self):
        username = self.telegram_username
        return username if username else f'{self.first_name} {self.last_name}'

    @classmethod
    def get_user_by_telegram_user_id(cls, session, telegram_user_id):
        return session.query(cls).filter(cls.telegram_user_id == telegram_user_id).first()


class CategoryEarning(Base):
    __tablename__ = 'category_earning'

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return f"<CategoryEarning('{self.id}', '{self.category}', '{self.user_id}')>"

    def __eq__(self, other):
        return isinstance(other, CategoryEarning) and other.id == self.id

    @classmethod
    def create_default_categories(cls, session, user_id):
        session.add(CategoryEarning(user_id=user_id, category='Зарплата🤑'))
        session.commit()

    @classmethod
    def get_all_categories(cls, session, user_id):
        return session.query(cls).filter(cls.user_id == user_id).all()

    @classmethod
    def get_all_categories_by_text(cls, session, user_id):
        categories = cls.get_all_categories(session, user_id)
        return [c.category for c in categories]

    @classmethod
    def add_category(cls, session, user_id, category: str):
        session.add(cls(category=category,
                        user_id=user_id))
        session.commit()

    def delete_category(self, session):
        earning_by_category = session.query(Earning).filter(self.id == Earning.category_id).all()
        Earning.delete_list_earning(session, earning_by_category)
        session.delete(self)
        session.commit()

    def update_category(self, session, new_category):
        self.category = new_category
        session.commit()


class Earning(Base):
    __tablename__ = 'earning'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    category_id = Column(Integer, ForeignKey('category_earning.id'))
    amount_money = Column(Float, default=0)

    def __repr__(self):
        return f"<Earning('{self.id}', '{self.user_id}', '{self.category_id}', " \
            f"'{self.amount_money}')>"

    def __eq__(self, other):
        return isinstance(other, Earning) and other.id == self.id

    @classmethod
    def delete_list_earning(cls, session, earnings: list):
        for e in earnings:
            session.delete(e)
        session.commit()


class CategoryConsumption(Base):
    __tablename__ = 'category_consumption'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    category = Column(String, nullable=False)

    def __repr__(self):
        return f"<CategoryConsumption('{self.id}', '{self.category}', '{self.user_id}')>"

    def __eq__(self, other):
        return isinstance(other, CategoryConsumption) and other.id == self.id

    @classmethod
    def get_all_categories(cls, session, user_id):
        return session.query(cls).filter(cls.user_id == user_id).all()

    @classmethod
    def get_all_categories_by_text(cls, session, user_id):
        categories = cls.get_all_categories(session, user_id)
        return [c.category for c in categories]

    @classmethod
    def add_category(cls, session, user_id, category: str):
        session.add(cls(category=category,
                        user_id=user_id))
        session.commit()

    @classmethod
    def create_default_categories(cls, session, user_id):
        session.add_all([CategoryConsumption(user_id=user_id, category='Продукты🍞'),
                         CategoryConsumption(user_id=user_id, category='Транспорт🚎'),
                         CategoryConsumption(user_id=user_id, category='Кафе🍕'),
                         CategoryConsumption(user_id=user_id, category='Подарки🎁'),
                         CategoryConsumption(user_id=user_id, category='Досуг🍿'),
                         CategoryConsumption(user_id=user_id, category='Покупки🛍'),
                         CategoryConsumption(user_id=user_id, category='Коммунальные🏠'),
                         CategoryConsumption(user_id=user_id, category='Здоровье💊')])
        session.commit()

    def delete_category(self, session):
        consumptions_by_category = session.query(Consumption).filter(self.id == Consumption.category_id).all()
        Consumption.delete_list_consumption(session, consumptions_by_category)
        session.delete(self)
        session.commit()

    def update_category(self, session, new_category):
        self.category = new_category
        session.commit()


class Consumption(Base):
    __tablename__ = 'consumption'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    category_id = Column(Integer, ForeignKey('category_consumption.id'))
    amount_money = Column(Float, default=0)

    def __repr__(self):
        return f"<Consumption('{self.id}', '{self.user_id}', '{self.category_id}', " \
            f"'{self.amount_money}')>"

    def __eq__(self, other):
        return isinstance(other, Consumption) and other.id == self.id

    @classmethod
    def delete_list_consumption(cls, session, consumptions: list):
        for c in consumptions:
            session.delete(c)
        session.commit()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
