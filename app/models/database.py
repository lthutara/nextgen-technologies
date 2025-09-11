from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from datetime import datetime
from typing import Optional
from sqlalchemy.sql import func
from config.settings import settings

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    content = Column(Text)
    summary = Column(Text)
    source_url = Column(String, unique=True, nullable=False)
    source_name = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)
    published_date = Column(DateTime)
    scraped_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    content_type = Column(String, nullable=True, default='news')

    def __repr__(self):
        return f"<Article(title='{self.title}', category='{self.category}')>"


class RawArticle(Base):
    __tablename__ = "raw_articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    content: Mapped[str] = mapped_column(Text)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_url: Mapped[str] = mapped_column(String, unique=True, index=True)
    source_name: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String, index=True)
    published_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    scraped_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    image_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    content_type: Mapped[Optional[str]] = mapped_column(String, nullable=True, default='news')


class ScrapingLog(Base):
    __tablename__ = "scraping_logs"

    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    articles_found = Column(Integer, default=0)
    articles_new = Column(Integer, default=0)
    status = Column(String, nullable=False)  # success, error, partial
    error_message = Column(Text)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)


# Database setup
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)