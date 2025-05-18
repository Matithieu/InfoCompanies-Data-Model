from sqlalchemy import Column, Index, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Leader(Base):
    __tablename__ = "leaders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    siren = Column(String)
    role = Column(String)
    last_name = Column(String)
    first_name = Column(String)
    gestion_number = Column(String)
    type = Column(String)
    event_name = Column(String)
    usage_name = Column(String)
    pseudo = Column(String)
    company_name = Column(String(3000))
    legal_form = Column(String)
    id_data = Column(String)

    __table_args__ = (
        Index("idx_leader_siren", "siren"),
        Index("idx_leader_company_name", "company_name"),
        Index("idx_leader_first_name", "first_name"),
        Index("idx_leader_last_name", "last_name"),
        Index("idx_leader_role", "role"),
    )
