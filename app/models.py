"""
SQLAlchemy Models
"""
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base


class Book(Base):
    """
    Book model representing a book entity in the database.
    
    Fields:
    - id: Primary key (auto-increment)
    - title: Book title (unique, non-null)
    - description: Book description (nullable)
    - author: Book author (non-null)
    - created_at: Timestamp of creation (auto-generated)
    - updated_at: Timestamp of last update (auto-updated)
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), unique=True, nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    author = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Enforce uniqueness constraint on title
    __table_args__ = (
        UniqueConstraint('title', name='uq_book_title'),
    )

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}')>"

