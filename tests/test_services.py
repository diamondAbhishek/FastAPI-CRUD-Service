"""
Unit Tests for Business Logic Services
"""
import pytest
from sqlalchemy.exc import IntegrityError

from app.services import (
    get_books_by_author_count,
    create_book_with_validation,
    bulk_create_books_transaction
)
from app.models import Book


def test_get_books_by_author_count(db_session, sample_book_data):
    """Test custom SQL query for getting authors with book count"""
    # Create test books
    book1 = Book(**sample_book_data)
    book2 = Book(title="Another Book", author="Test Author", description="Description 2")
    book3 = Book(title="Third Book", author="Different Author", description="Description 3")
    
    db_session.add_all([book1, book2, book3])
    db_session.commit()
    
    # Test aggregation query
    result = get_books_by_author_count(db_session, min_books=1)
    
    # Verify results
    assert len(result) == 2  # Two authors
    assert any(r["author"] == "Test Author" and r["book_count"] == 2 for r in result)
    assert any(r["author"] == "Different Author" and r["book_count"] == 1 for r in result)


def test_create_book_with_validation_success(db_session):
    """Test successful book creation with validation"""
    book = create_book_with_validation(
        db_session,
        title="Valid Book",
        author="Valid Author",
        description="Valid description"
    )
    
    assert book.id is not None
    assert book.title == "Valid Book"
    assert book.author == "Valid Author"


def test_create_book_with_validation_empty_title(db_session):
    """Test validation error for empty title"""
    with pytest.raises(ValueError, match="Title cannot be empty"):
        create_book_with_validation(
            db_session,
            title="",
            author="Valid Author"
        )


def test_create_book_with_validation_empty_author(db_session):
    """Test validation error for empty author"""
    with pytest.raises(ValueError, match="Author cannot be empty"):
        create_book_with_validation(
            db_session,
            title="Valid Title",
            author=""
        )


def test_create_book_with_validation_duplicate_title(db_session):
    """Test validation error for duplicate title"""
    # Create first book
    create_book_with_validation(
        db_session,
        title="Duplicate Title",
        author="Author 1"
    )
    
    # Try to create another book with same title
    with pytest.raises(ValueError, match="already exists"):
        create_book_with_validation(
            db_session,
            title="Duplicate Title",
            author="Author 2"
        )


def test_bulk_create_books_transaction_success(db_session):
    """Test successful bulk creation in a transaction"""
    books_data = [
        {"title": "Book 1", "author": "Author 1", "description": "Desc 1"},
        {"title": "Book 2", "author": "Author 2", "description": "Desc 2"},
        {"title": "Book 3", "author": "Author 3", "description": "Desc 3"},
    ]
    
    books = bulk_create_books_transaction(db_session, books_data)
    
    assert len(books) == 3
    assert all(book.id is not None for book in books)
    
    # Verify all books are in database
    count = db_session.query(Book).count()
    assert count == 3


def test_bulk_create_books_transaction_rollback(db_session):
    """Test transaction rollback on error"""
    books_data = [
        {"title": "Book 1", "author": "Author 1", "description": "Desc 1"},
        {"title": "Book 1", "author": "Author 2", "description": "Desc 2"},  # Duplicate title
    ]
    
    # Transaction should rollback on integrity error
    with pytest.raises(Exception):
        bulk_create_books_transaction(db_session, books_data)
    
    # Verify no books were created (transaction rolled back)
    count = db_session.query(Book).count()
    assert count == 0

