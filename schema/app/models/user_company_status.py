import enum

from sqlalchemy import Column, Enum, Index, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Status(enum.Enum):
    NOT_DONE = "NOT_DONE"
    TO_DO = "TO_DO"
    DONE = "DONE"


class UserCompanyStatus(Base):
    __tablename__ = "user_company_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    status = Column(Enum(Status))
    company_id = Column(Integer)

    __table_args__ = (
        Index("ix_user_company_status_user_id", "user_id"),
        Index("ix_user_company_status_company_id", "company_id"),
    )
