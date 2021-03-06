import datetime
import enum

from sqlalchemy import Integer, Column, String, ForeignKey, create_engine, Float, DateTime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, validates

from contextlib import contextmanager

engine = create_engine('sqlite:///database.db', echo=False)
Base = declarative_base()

Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    telegram_username = Column(String)
    telegram_user_id = Column(Integer, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    last_activity = Column(DateTime)
    date_registration = Column(DateTime,)

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
        if username:
            return username
        elif self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return f'{self.first_name}'

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
    time_creation = Column(DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return f"<Earning('{self.id}', '{self.user_id}', '{self.category_id}', " \
            f"'{self.amount_money}', '{self.time_creation}')>"

    def __eq__(self, other):
        return isinstance(other, Earning) and other.id == self.id

    @classmethod
    def delete_list_earning(cls, session, earnings: list):
        for e in earnings:
            session.delete(e)
        session.commit()

    def get_str_time_creation(self):
        return datetime.datetime.strftime(self.time_creation, '%d.%m.%Y, %H:%M')


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
    time_creation = Column(DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return f"<Consumption('{self.id}', '{self.user_id}', '{self.category_id}', " \
            f"'{self.amount_money}', '{self.time_creation}')>"

    def __eq__(self, other):
        return isinstance(other, Consumption) and other.id == self.id

    def get_str_time_creation(self):
        return datetime.datetime.strftime(self.time_creation, '%d.%m.%Y, %H:%M')

    @classmethod
    def delete_list_consumption(cls, session, consumptions: list):
        for c in consumptions:
            session.delete(c)
        session.commit()


class TypeLimit(enum.Enum):
    DAILY, WEEKLY, MONTHLY = range(3)

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def text_type(cls, value):
        if value == cls.DAILY.value:
            return 'суточный'
        elif value == cls.WEEKLY.value:
            return 'недельный'
        elif value == cls.MONTHLY.value:
            return 'месячный'


class Limit(Base):
    __tablename__ = 'limit'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    type_limit = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey('category_consumption.id'), nullable=True)
    amount_money = Column(Integer, default=0)

    @validates('type_limit')
    def validate_type_limit(self, key, value):
        assert TypeLimit.has_value(value)
        return value

    @classmethod
    def add(cls, session, user_id, type_limit, category_id, amount_money):
        session.add(Limit(user_id=user_id, type_limit=type_limit,
                          category_id=category_id, amount_money=amount_money))
        session.commit()

    @classmethod
    def get_limits_by_type(cls, session, user_id, type_limit: int):
        return session.query(cls).filter(
            cls.user_id == user_id,
            cls.type_limit == type_limit
        ).all()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
