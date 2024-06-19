from sqlalchemy import TEXT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import VARCHAR

class BaseModel(DeclarativeBase):
    pass

class Illness(BaseModel):
    __tablename__ = 'illness'
    
    id: Mapped[str] = mapped_column(VARCHAR(1), primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(VARCHAR(32), nullable=False)

class Goals(BaseModel):
    __tablename__ = 'goals'
    
    id: Mapped[str] = mapped_column(VARCHAR(1), primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(VARCHAR(32), nullable=False)
    description: Mapped[str] = mapped_column(TEXT, nullable=False)

class Commitment(BaseModel):
    __tablename__ = 'commitment'
    
    id: Mapped[str] = mapped_column(VARCHAR(1), primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(VARCHAR(32), nullable=False)