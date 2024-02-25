import datetime
import uuid

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, UUID, Enum
from sqlalchemy.orm import declarative_base, relationship

from src.db import enums

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    chat_id = Column(Integer, nullable=False)
    subscription = relationship('Subscription', backref='user', uselist=False)


class City(Base):
    __tablename__ = 'cities'
    id = Column(String(50), primary_key=True)
    aima_id = Column(ForeignKey('aima.id'))


class AIMA(Base):
    __tablename__ = 'aima'
    id = Column(String(50), primary_key=True)
    city = relationship('City', backref='aima', uselist=False)
    subscriptions = relationship('Subscription', backref='aima')


class Article(Base):
    __tablename__ = 'articles'
    id = Column(String(30), primary_key=True)
    subscriptions = relationship('Subscription', backref='article')


class Subscription(Base):
    __tablename__ = 'subscriptions'
    user_id = Column(ForeignKey('users.id'), primary_key=True)
    date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    aima_id = Column(ForeignKey('aima.id'), nullable=False)
    article_id = Column(ForeignKey('articles.id'), nullable=False)


class Status(Base):
    __tablename__ = 'statuses'
    created_at = Column(DateTime, default=datetime.datetime.now)
    id = Column(UUID(as_uuid=True), primary_key=True, default=str(uuid.uuid4()), server_default=str(uuid.uuid4()))
    subscription_id = Column(ForeignKey('subscriptions.user_id'), nullable=False, index=True)
    status = Column(Enum(enums.StatusesEnum), nullable=False)
