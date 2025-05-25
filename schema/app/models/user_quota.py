from sqlalchemy import Column, Index, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserQuota(Base):
    __tablename__ = "user_quota"

    user_id = Column(String, primary_key=True)
    quota_allocated = Column(Integer)
    quota_used = Column(Integer)

    __table_args__ = (
        Index("ix_user_quota_user_id", "user_id"),
        Index("ix_user_quota_quota_allocated", "quota_allocated"),
        Index("ix_user_quota_quota_used", "quota_used"),
    )
