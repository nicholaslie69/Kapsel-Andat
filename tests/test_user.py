from fastapi.testclient import TestClient
from main import app
from modules.users.routes.create_user import users_db

client = TestClient(app)

def setup_function():
    users_db.clear()
    global next_user_id
    from modules.users.routes.create_user import next_user_id
    modules.users.routes.create_user.next_user_id = 1
    
    client.post("/users/", json={
        "username": "adminuser", 
        "email": "admin@example.com", 
        "password": "Admin!Password1", 
        "role": "admin"
    })
    client.post("/users/", json={
        "username": "staffuser", 
        "email": "staff@example.com", 
        "password": "Staff!Password1", 
        "role": "staff"
    })

def test_create_user_success():
    """Test skenario sukses membuat user baru."""
    payload = {
        "username": "newuser7", 
        "email": "newuser@test.com", 
        "password": "User!Password1", 
        "role": "staff"
    }
    response = client.post("/users/", json=payload)
    
    assert response.status_code == 201
    assert response.json()["success"] == True
    assert response.json()["data"]["username"] == "newuser7"
    assert response.json()["data"]["id"] == 3

def test_create_user_validation_error():
    """Test validasi error (Username terlalu pendek). [cite: 6]"""
    payload = {
        "username": "short",
        "email": "invalid@test.com", 
        "password": "Valid!Password1", 
        "role": "staff"
    }
    response = client.post("/users/", json=payload)
    
    assert response.status_code == 422

def test_create_user_password_error():
    """Test validasi error (Password tidak ada karakter khusus). [cite: 8, 12]"""
    payload = {
        "username": "testuser1",
        "email": "test@test.com", 
        "password": "Password123",
        "role": "staff"
    }
    response = client.post("/users/", json=payload)
    
    assert response.status_code == 422

def test_read_all_users_admin_success():
    """Admin berhasil membaca semua user. [cite: 20]"""
    response = client.get("/users/", params={"auth_username": "adminuser"}) 
    
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert len(response.json()["data"]) == 2

def test_read_all_users_staff_forbidden():
    """Staff gagal membaca semua user (Forbidden). [cite: 20, 21]"""
    response = client.get("/users/", params={"auth_username": "staffuser"})
    
    assert response.status_code == 403

def test_read_own_user_staff_success():
    """Staff berhasil membaca data miliknya sendiri (ID 2). [cite: 21]"""
    response = client.get("/users/2", params={"auth_username": "staffuser"}) 
    
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 2
    assert response.json()["data"]["username"] == "staffuser"

def test_read_other_user_staff_forbidden():
    """Staff gagal membaca data user lain (ID 1). [cite: 21]"""
    response = client.get("/users/1", params={"auth_username": "staffuser"}) 
    
    assert response.status_code == 403

def test_read_any_user_admin_success():
    """Admin berhasil membaca data user lain (ID 2). [cite: 20]"""
    response = client.get("/users/2", params={"auth_username": "adminuser"}) 
    
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 2

def test_update_user_admin_success():
    """Admin berhasil update user lain (ID 2). [cite: 20]"""
    update_payload = {
        "username": "newstaff", 
        "email": "new.staff@test.com", 
        "password": "New!Password1", 
        "role": "staff"
    }
    response = client.put("/users/2", params={"auth_username": "adminuser"}, json=update_payload)
    
    assert response.status_code == 200
    assert response.json()["data"]["username"] == "newstaff"

def test_update_user_staff_forbidden():
    """Staff gagal update user (Forbidden). [cite: 20]"""
    update_payload = {
        "username": "newstaff", 
        "email": "new.staff@test.com", 
        "password": "New!Password1", 
        "role": "staff"
    }
    response = client.put("/users/2", params={"auth_username": "staffuser"}, json=update_payload)
    
    assert response.status_code == 403

def test_delete_user_admin_success():
    """Admin berhasil menghapus user (ID 2). [cite: 20]"""
    response = client.delete("/users/2", params={"auth_username": "adminuser"})
    
    assert response.status_code == 200
    assert response.json()["message"] == "User ID 2 successfully deleted"
    
    response_read = client.get("/users/2", params={"auth_username": "adminuser"})
    assert response_read.status_code == 404

def test_delete_user_staff_forbidden():
    """Staff gagal menghapus user (Forbidden). [cite: 20]"""
    response = client.delete("/users/2", params={"auth_username": "staffuser"})
    
    assert response.status_code == 403