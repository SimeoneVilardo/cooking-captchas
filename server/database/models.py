import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from database.core import Base


class DBCaptcha(Base):
    __tablename__ = "captchas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    value = Column(String, index=True)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
