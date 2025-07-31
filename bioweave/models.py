
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
from .config import settings

engine = create_engine(settings.database_url, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Upload(Base):
    __tablename__ = "uploads"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    status = Column(String, default="processing")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    report = Column(JSON, nullable=True)
    dataset_path = Column(String, nullable=True)

def init_db():
    Base.metadata.create_all(bind=engine)
