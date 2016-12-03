from sqlalchemy import Column, Integer, String, Text, DateTime

from .database import Base

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    sender = Column(String(64))
    timestamp = Column(DateTime)
    content = Column(Text)
    size = Column(Integer)
    pos_x = Column(Integer)
    pos_y = Column(Integer)
    pos_z = Column(Integer)
