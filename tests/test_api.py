"""
Integration Tests for API Endpoints
"""
import pytest


def test_create_item(client, sample_book_data):
    """Test POST /items/ - Create a new book"""
    response = client.post("/api/v1/items/", json=sample_book_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == sample_book_data["title"]
    assert data["author"] == sample_book_data["author"]
    assert data["id"] is not None
    assert "created_at" in data


def test_create_item_duplicate_title(client, sample_book_data):
    """Test POST /items/ - Create duplicate book (should fail)"""
    # Create first book
    client.post("/api/v1/items/", json=sample_book_data)
    
    # Try to create duplicate
    response = client.post("/api/v1/items/", json=sample_book_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_list_items_empty(client):
    """Test GET /items/ - Empty list"""
    response = client.get("/api/v1/items/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []
    assert data["page"] == 1
    assert data["page_size"] == 10


def test_list_items_with_pagination(client):
    """Test GET /items/ - Pagination"""
    # Create multiple books
    for i in range(15):
        client.post("/api/v1/items/", json={
            "title": f"Book {i}",
            "author": f"Author {i}",
            "description": f"Description {i}"
        })
    
    # Test first page
    response = client.get("/api/v1/items/?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 10
    assert data["total"] == 15
    assert data["page"] == 1
    assert data["total_pages"] == 2
    
    # Test second page
    response = client.get("/api/v1/items/?page=2&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 5
    assert data["page"] == 2


def test_list_items_filter_by_author(client):
    """Test GET /items/ - Filter by author"""
    # Create books with different authors
    client.post("/api/v1/items/", json={
        "title": "Book 1",
        "author": "John Doe",
        "description": "Description 1"
    })
    client.post("/api/v1/items/", json={
        "title": "Book 2",
        "author": "Jane Smith",
        "description": "Description 2"
    })
    client.post("/api/v1/items/", json={
        "title": "Book 3",
        "author": "John Doe",
        "description": "Description 3"
    })
    
    # Filter by author
    response = client.get("/api/v1/items/?author=John")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert all("John" in item["author"] for item in data["items"])


def test_get_item(client, sample_book_data):
    """Test GET /items/{id} - Get single book"""
    # Create a book
    create_response = client.post("/api/v1/items/", json=sample_book_data)
    book_id = create_response.json()["id"]
    
    # Get the book
    response = client.get(f"/api/v1/items/{book_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == book_id
    assert data["title"] == sample_book_data["title"]


def test_get_item_not_found(client):
    """Test GET /items/{id} - Non-existent book"""
    response = client.get("/api/v1/items/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_update_item(client, sample_book_data):
    """Test PUT /items/{id} - Update book"""
    # Create a book
    create_response = client.post("/api/v1/items/", json=sample_book_data)
    book_id = create_response.json()["id"]
    
    # Update the book
    update_data = {
        "title": "Updated Title",
        "author": "Updated Author",
        "description": "Updated description"
    }
    response = client.put(f"/api/v1/items/{book_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["author"] == "Updated Author"


def test_update_item_not_found(client):
    """Test PUT /items/{id} - Non-existent book"""
    response = client.put("/api/v1/items/999", json={"title": "New Title"})
    assert response.status_code == 404


def test_partial_update_item(client, sample_book_data):
    """Test PATCH /items/{id} - Partial update"""
    # Create a book
    create_response = client.post("/api/v1/items/", json=sample_book_data)
    book_id = create_response.json()["id"]
    
    # Partial update (only title)
    update_data = {"title": "Partially Updated Title"}
    response = client.patch(f"/api/v1/items/{book_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Partially Updated Title"
    assert data["author"] == sample_book_data["author"]  # Unchanged


def test_delete_item(client, sample_book_data):
    """Test DELETE /items/{id} - Delete book"""
    # Create a book
    create_response = client.post("/api/v1/items/", json=sample_book_data)
    book_id = create_response.json()["id"]
    
    # Delete the book
    response = client.delete(f"/api/v1/items/{book_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/items/{book_id}")
    assert get_response.status_code == 404


def test_delete_item_not_found(client):
    """Test DELETE /items/{id} - Non-existent book"""
    response = client.delete("/api/v1/items/999")
    assert response.status_code == 404


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

