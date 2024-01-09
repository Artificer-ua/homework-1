import configparser
# import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from headers import CONFIG_FILE

# file_config = pathlib.Path(__file__).parent.parent.joinpath(CONFIG_FILE)
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

username = config.get("DB", "USER")
password = config.get("DB", "PASSWORD")
db_name = config.get("DB", "DB_NAME")
domain = config.get("DB", "DOMAIN")
port = config.get("DB", "PORT")

# postgresql+psycopg2://postgres:pass@10.10.5.13:5432/pyweb
# protocol://username:password@host:port/db_name
URL = f"postgresql+psycopg2://{username}:{password}@{domain}/{db_name}"

Base = declarative_base()

engine = create_engine(URL, echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()
