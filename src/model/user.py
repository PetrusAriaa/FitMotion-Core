import uuid
from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, DATE
from sqlalchemy.dialects.postgresql.pg_catalog import func

class BaseModel(DeclarativeBase):
    pass

class UserModel(BaseModel):
    __tablename__ = 'users'
    
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True, server_default=str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(String(32), unique=True)
    display_name: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[DateTime] = mapped_column(DATE, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DATE, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(nullable=True)
    