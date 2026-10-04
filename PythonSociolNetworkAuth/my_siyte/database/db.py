from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine  import create_engine
from sqlalchemy.ext.declarative import declarative_base



SQLALCHEMY_DATABASE_URL = 'sqlite:///./database.sqlite3'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)
Base =  declarative_base()