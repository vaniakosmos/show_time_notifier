from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.settings import DATABASE_URL, DEBUG


engine = create_engine(DATABASE_URL, echo=DEBUG)
Model = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
