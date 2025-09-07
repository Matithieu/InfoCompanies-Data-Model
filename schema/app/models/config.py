from sqlalchemy import Column, Date, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Config(Base):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True, autoincrement=True)
    last_reset_quota_date = Column(Date)
