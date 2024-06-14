import uuid
from sqlalchemy import DateTime, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, DATE, SMALLINT
from sqlalchemy.dialects.postgresql.pg_catalog import func

class BaseModel(DeclarativeBase):
    pass

class Friends(BaseModel):
    __tablename__ = 'friends'
    
    id: Mapped[int] = mapped_column(SMALLINT, primary_key=True, unique=True, server_default=text("nextval('friends_id_seq'::regclass)"))
    fk_user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False)
    friend_id: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DATE, nullable=False)

class FriendRequests(BaseModel):
    __tablename__ = 'friend_requests'
    
    id: Mapped[str] = mapped_column(SMALLINT, primary_key=True, unique=True, server_default=text("nextval('friend_requests_id_seq'::regclass)"))
    fk_user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False)
    friend_id: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DATE, nullable=False)