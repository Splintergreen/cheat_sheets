from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
import os
from dotenv import load_dotenv

load_dotenv()

db_name = os.getenv('db_name')
db_username = os.getenv('db_username')
db_pass = os.getenv('db_pass')
db_host = os.getenv('db_host')
db_port = os.getenv('db_port')


engine = create_engine(
    f'postgresql+psycopg2://{db_username}:{db_pass}@{db_host}:{db_port}/{db_name}'
    )
Base = declarative_base()


class Note(Base):
    __tablename__ = 'note'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    date = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.current_date()
        )


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()
