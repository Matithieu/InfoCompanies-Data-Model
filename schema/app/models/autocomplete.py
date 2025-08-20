from sqlalchemy import Column, Index, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    __table_args__ = (Index("ix_city_name", "name"),)


class IndustrySector(Base):
    __tablename__ = "industry_sector"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    __table_args__ = (Index("ix_industry_sector_name", "name"),)


class LegalForm(Base):
    __tablename__ = "legal_form"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    __table_args__ = (Index("ix_legal_form_name", "name"),)


class Region(Base):
    __tablename__ = "region"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    __table_args__ = (Index("ix_region_name", "name"),)
