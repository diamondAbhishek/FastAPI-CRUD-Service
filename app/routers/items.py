"""
Items Router - CRUD endpoints for books
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import Book
from app.schemas import BookCreate, BookUpdate, BookResponse, BookListResponse

router = APIRouter()


@router.post("/items/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_item(book: BookCreate, db: Session = Depends(get_db)):
    """
    Create a new book item.
    
    - **title**: Book title (must be unique)
    - **description**: Book description (optional)
    - **author**: Book author
    
    Returns the created book with generated id and timestamps.
    """
    try:
        db_book = Book(**book.model_dump())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Book with title '{book.title}' already exists"
        )


@router.get("/items/", response_model=BookListResponse)
async def list_items(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    author: Optional[str] = Query(None, description="Filter by author"),
    db: Session = Depends(get_db)
):
    """
    Get a paginated list of books with optional filtering by author.
    
    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 10, max: 100)
    - **author**: Optional filter by author name
    
    Returns paginated list with metadata.
    """
    # Custom SQL query: Filter and count with conditional author filtering
    query = db.query(Book)
    
    # Apply filter if author is provided
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))  # Case-insensitive search
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    skip = (page - 1) * page_size
    total_pages = (total + page_size - 1) // page_size  # Ceiling division
    
    # Apply pagination
    books = query.offset(skip).limit(page_size).all()
    
    return BookListResponse(
        items=books,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/items/{item_id}", response_model=BookResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get a single book by ID.
    
    - **item_id**: The ID of the book to retrieve
    
    Returns 404 if book not found.
    """
    book = db.query(Book).filter(Book.id == item_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {item_id} not found"
        )
    return book


@router.put("/items/{item_id}", response_model=BookResponse)
async def update_item(item_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    """
    Update a book item (full update - all fields).
    
    - **item_id**: The ID of the book to update
    - **book_update**: Updated book data (all fields optional)
    
    Returns 404 if book not found, 400 if title already exists.
    """
    db_book = db.query(Book).filter(Book.id == item_id).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {item_id} not found"
        )
    
    try:
        # Update only provided fields
        update_data = book_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_book, field, value)
        
        db.commit()
        db.refresh(db_book)
        return db_book
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with this title already exists"
        )


@router.patch("/items/{item_id}", response_model=BookResponse)
async def partial_update_item(item_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    """
    Partially update a book item.
    
    - **item_id**: The ID of the book to update
    - **book_update**: Updated book data (only provided fields will be updated)
    
    Returns 404 if book not found, 400 if title already exists.
    """
    # PATCH is similar to PUT but we only update provided fields
    return await update_item(item_id, book_update, db)


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete a book item.
    
    - **item_id**: The ID of the book to delete
    
    Returns 404 if book not found, 204 on successful deletion.
    """
    db_book = db.query(Book).filter(Book.id == item_id).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {item_id} not found"
        )
    
    db.delete(db_book)
    db.commit()
    return None

