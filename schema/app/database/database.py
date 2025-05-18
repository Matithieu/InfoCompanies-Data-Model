from logging.config import fileConfig
from sqlalchemy import create_engine, text
import configparser  # Use ConfigParser for reading config

from app.models.autocomplete import Base as AutocompleteBase
from app.models.companies import Base as CompaniesBase
from app.models.config import Base as ConfigBase
from app.models.leaders import Base as LeadersBase
from app.models.user_company_status import Base as UserCompanyStatusBase
from app.models.user_quota import Base as UserQuotaBase


# Replace Alembic context with custom config handling
config = configparser.ConfigParser()

# Load the configuration file (you can change this path to your actual config file)
config.read("alembic.ini")  # Replace with the correct path if necessary

# Retrieve the sqlalchemy.url from the config file
url = config.get(
    "alembic", "sqlalchemy.url"
)  # Assuming your config has a section [database] with sqlalchemy.url

# SQLAlchemy engine setup
engine = create_engine(url)


def ensure_pg_trgm(connection):
    if connection.dialect.name == "postgresql":
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))


def create_trgm_index(connection):
    if connection.dialect.name == "postgresql":
        connection.execute(
            text(
                """
                CREATE INDEX IF NOT EXISTS idx_companies_company_name_trgm 
                ON companies USING gin (LOWER(company_name) gin_trgm_ops);
                """
            )
        )


def init_db():
    # Create tables
    bases = [
        CompaniesBase,
        LeadersBase,
        ConfigBase,
        AutocompleteBase,
        UserQuotaBase,
        UserCompanyStatusBase,
    ]

    for base in bases:
        base.metadata.create_all(engine)

    with engine.begin() as conn:
        ensure_pg_trgm(conn)
        create_trgm_index(conn)


if __name__ == "__main__":
    init_db()
