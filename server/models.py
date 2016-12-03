from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from server.database import Base

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    sender = Column(String(64))
    timestamp = Column(DateTime, server_default=func.now())
    content_type = Column(String(16))
    content = Column(Text)
    size = Column(String(32))
    pos_x = Column(Integer)
    pos_y = Column(Integer)
    pos_z = Column(Integer)
