from sqlalchemy import Column, Date, Float, Index, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String)
    siren_number = Column(String)
    nic_number = Column(String)
    legal_form = Column(String)
    ape_code = Column(String)
    ape_label = Column(String)
    address = Column(String)
    postal_code = Column(String)
    department_number = Column(String)
    department = Column(String)
    city = Column(String)
    region = Column(String)
    trade_name = Column(String)

    registration_date = Column(Date)
    deregistration_date = Column(Date)

    # 2018
    closing_date_2018_1 = Column(Date)
    revenue_2018_1 = Column(Float)
    turnover_2018_1 = Column(Float)
    closing_date_2018_2 = Column(Date)
    revenue_2018_2 = Column(Float)
    turnover_2018_2 = Column(Float)
    closing_date_2018_3 = Column(Date)
    revenue_2018_3 = Column(Float)
    turnover_2018_3 = Column(Float)

    # 2019
    closing_date_2019_1 = Column(Date)
    revenue_2019_1 = Column(Float)
    turnover_2019_1 = Column(Float)
    closing_date_2019_2 = Column(Date)
    revenue_2019_2 = Column(Float)
    turnover_2019_2 = Column(Float)
    closing_date_2019_3 = Column(Date)
    revenue_2019_3 = Column(Float)
    turnover_2019_3 = Column(Float)

    # 2020
    closing_date_2020_1 = Column(Date)
    revenue_2020_1 = Column(Float)
    turnover_2020_1 = Column(Float)
    closing_date_2020_2 = Column(Date)
    revenue_2020_2 = Column(Float)
    turnover_2020_2 = Column(Float)
    closing_date_2020_3 = Column(Date)
    revenue_2020_3 = Column(Float)
    turnover_2020_3 = Column(Float)

    # 2021
    closing_date_2021_1 = Column(Date)
    revenue_2021_1 = Column(Float)
    turnover_2021_1 = Column(Float)
    closing_date_2021_2 = Column(Date)
    revenue_2021_2 = Column(Float)
    turnover_2021_2 = Column(Float)
    closing_date_2021_3 = Column(Date)
    revenue_2021_3 = Column(Float)
    turnover_2021_3 = Column(Float)

    # 2022
    closing_date_2022_1 = Column(Date)
    revenue_2022_1 = Column(Float)
    turnover_2022_1 = Column(Float)
    closing_date_2022_2 = Column(Date)
    revenue_2022_2 = Column(Float)
    turnover_2022_2 = Column(Float)
    closing_date_2022_3 = Column(Date)
    revenue_2022_3 = Column(Float)
    turnover_2022_3 = Column(Float)

    # 2023
    closing_date_2023_1 = Column(Date)
    revenue_2023_1 = Column(Float)
    turnover_2023_1 = Column(Float)
    closing_date_2023_2 = Column(Date)
    revenue_2023_2 = Column(Float)
    turnover_2023_2 = Column(Float)
    closing_date_2023_3 = Column(Date)
    revenue_2023_3 = Column(Float)
    turnover_2023_3 = Column(Float)

    industry_sector = Column(String)
    phone_number = Column(String)
    website = Column(String(3000))

    reviews = Column(JSONB)
    schedule = Column(JSONB)

    instagram = Column(String(10000))
    facebook = Column(String(3000))
    twitter = Column(String(3000))
    linkedin = Column(String(3000))
    youtube = Column(String(3000))
    email = Column(String(3000))

    scraping_date = Column(Date)
    date_creation = Column(Date)
    last_processing_date = Column(Date)
    number_of_employee = Column(Integer)
    company_category = Column(String)

    __table_args__ = (
        # Single column indexes
        Index("ix_companies_siren_number", "siren_number"),
        Index("ix_companies_company_name", "company_name"),
        Index("ix_companies_legal_form", "legal_form"),
        Index("ix_companies_industry_sector", "industry_sector"),
        Index("ix_companies_region", "region"),
        Index("ix_companies_city", "city"),
        Index("ix_companies_phone_number", "phone_number"),
        Index("ix_companies_website", "website"),
        Index("ix_companies_email", "email"),
        Index("ix_companies_number_of_employee", "number_of_employee"),
        Index("ix_companies_linkedin", "linkedin"),
        Index("ix_companies_twitter", "twitter"),
        Index("ix_companies_facebook", "facebook"),
        Index("ix_companies_instagram", "instagram"),
        Index("ix_companies_youtube", "youtube"),
        #
        # Composite indexes
        Index(
            "ix_companies_region_city_industry_sector_legal_form",
            "region",
            "city",
            "industry_sector",
            "legal_form",
        ),
        Index(
            "ix_companies_region_city_industry_sector",
            "region",
            "city",
            "industry_sector",
        ),
        Index("ix_companies_region_city_legal_form", "region", "city", "legal_form"),
        Index("ix_companies_region_city", "region", "city"),
        Index("ix_companies_region_industry_sector", "region", "industry_sector"),
        Index("ix_companies_region_legal_form", "region", "legal_form"),
        Index(
            "ix_companies_city_industry_sector_legal_form",
            "city",
            "industry_sector",
            "legal_form",
        ),
        Index("ix_companies_city_industry_sector", "city", "industry_sector"),
        Index("ix_companies_city_legal_form", "city", "legal_form"),
        Index(
            "ix_companies_region_industry_sector_legal_form",
            "region",
            "industry_sector",
            "legal_form",
        ),
        Index(
            "ix_companies_industry_sector_legal_form", "industry_sector", "legal_form"
        ),
        Index(
            "ix_companies_industry_sector_number_of_employee",
            "industry_sector",
            "number_of_employee",
        ),
    )
