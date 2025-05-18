from sqlalchemy import BigInteger, Column, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Config(Base):
    __tablename__ = "config"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    last_reset_quota_date = Column(Date)
