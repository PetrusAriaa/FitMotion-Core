from datetime import datetime
from sqlalchemy import DateTime, String, Boolean, Date, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP

class BaseModel(DeclarativeBase):
    pass

class Users(BaseModel):
    __tablename__ = 'users'
    
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(TIMESTAMP, nullable=False, default=datetime.now())
    updated_at: Mapped[DateTime] = mapped_column(TIMESTAMP)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    last_login: Mapped[DateTime] = mapped_column(TIMESTAMP)
    verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    weight: Mapped[float] = mapped_column(Float)
    height: Mapped[float] = mapped_column(Float)
    birth: Mapped[DateTime] = mapped_column(Date)
    fk_goal: Mapped[str] = mapped_column(String(1))
    fk_illness: Mapped[str] = mapped_column(String(1))