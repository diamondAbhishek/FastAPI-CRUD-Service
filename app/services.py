"""
Business Logic Services
This module contains reusable business logic functions.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.models import Book


def get_books_by_author_count(db: Session, min_books: int = 1) -> List[dict]:
    """
    Custom SQL query: Get authors with book count using aggregation.
    
    This demonstrates a custom SQL query through the ORM with aggregation.
    
    Args:
        db: Database session
        min_books: Minimum number of books an author must have
    
    Returns:
        List of dictionaries with author name and book count
    """
    result = (
        db.query(
            Book.author,
            func.count(Book.id).label('book_count')
        )
        .group_by(Book.author)
        .having(func.count(Book.id) >= min_books)
        .order_by(func.count(Book.id).desc())
        .all()
    )
    
    return [
        {"author": author, "book_count": count}
        for author, count in result
    ]


def create_book_with_validation(
    db: Session,
    title: str,
    author: str,
    description: Optional[str] = None
) -> Book:
    """
    Business logic function to create a book with validation.
    
    This function demonstrates transaction handling and validation logic.
    
    Args:
        db: Database session
        title: Book title
        author: Book author
        description: Optional book description
    
    Returns:
        Created Book object
    
    Raises:
        ValueError: If validation fails
    """
    # Validation logic
    if not title or not title.strip():
        raise ValueError("Title cannot be empty")
    
    if not author or not author.strip():
        raise ValueError("Author cannot be empty")
    
    if len(title) > 200:
        raise ValueError("Title exceeds maximum length of 200 characters")
    
    # Check if book with same title exists
    existing_book = db.query(Book).filter(Book.title == title).first()
    if existing_book:
        raise ValueError(f"Book with title '{title}' already exists")
    
    # Create and return book within transaction
    book = Book(title=title.strip(), author=author.strip(), description=description)
    db.add(book)
    db.commit()
    db.refresh(book)
    
    return book


def bulk_create_books_transaction(
    db: Session,
    books_data: List[dict]
) -> List[Book]:
    """
    Demonstrate transaction handling: Create multiple books in a single transaction.
    
    If any book creation fails, the entire transaction is rolled back.
    
    Args:
        db: Database session
        books_data: List of dictionaries with book data (title, author, description)
    
    Returns:
        List of created Book objects
    
    Raises:
        Exception: If any book creation fails, rolls back entire transaction
    """
    try:
        books = []
        for book_data in books_data:
            book = Book(**book_data)
            db.add(book)
            books.append(book)
        
        # Commit all books in a single transaction
        db.commit()
        
        # Refresh all books to get IDs
        for book in books:
            db.refresh(book)
        
        return books
    except Exception as e:
        # Rollback entire transaction on any error
        db.rollback()
        raise e

