import enum

from sqlalchemy import BigInteger, Column, Enum, Index, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Status(enum.Enum):
    NOT_DONE = "NOT_DONE"
    TO_DO = "TO_DO"
    DONE = "DONE"


class UserCompanyStatus(Base):
    __tablename__ = "user_company_status"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String)
    status = Column(Enum(Status))
    company_id = Column(BigInteger)

    __table_args__ = (
        Index("ix_user_company_status_user_id", "user_id"),
        Index("ix_user_company_status_company_id", "company_id"),
    )
