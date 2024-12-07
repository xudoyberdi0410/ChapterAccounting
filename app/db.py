from sqlalchemy import create_engine, Column, String, Integer, CHAR, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Chapters(Base):
    __tablename__ = 'chapters'
    ch_id = Column("id", Integer, primary_key=True)
    title_name = Column("title_name", String)
    chapter = Column("chapter", Integer)
    position = Column("position", String, nullable=True)
    created_at = Column("created_at", DateTime, default=datetime.datetime.now)

    def __init__(self, title_name, chapter, position):
        self.title_name = title_name
        self.chapter = chapter
        self.position = position

    def __repr__(self):
        return f"<Chapter(title_name={self.title_name}, chapter={self.chapter}, position={self.position}, created_at={self.created_at})>"

    def to_dict(self):
        d = self.__dict__.copy()
        if "_sa_instance_state" in d:
            del d["_sa_instance_state"]
        return d
engine = create_engine("sqlite:///manga.db", echo=True)
# Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
