import uuid
from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, DATE
from sqlalchemy.dialects.postgresql.pg_catalog import func

class BaseModel(DeclarativeBase):
    pass

class FriendsModel(BaseModel):
    __tablename__ = 'friends'
    
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True, server_default=str(uuid.uuid4()))
    fk_user_id: Mapped[str] = mapped_column(UUID(as_uuid=True))
    fk_friend_id: Mapped[str] = mapped_column(UUID(as_uuid=True))
    created_at: Mapped[DateTime] = mapped_column(DATE, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DATE, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(nullable=True)
    prev_id: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=True)