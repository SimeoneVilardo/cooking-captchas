from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from database.core import Base as Base


class DBCaptcha(Base):
    __tablename__ = "captchas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    value: Mapped[str] = mapped_column(String, index=True)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
