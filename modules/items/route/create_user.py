from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime
from modules.users.schema.schemas import User, UserIn, UserResponse, Role

router = APIRouter(tags=["Users"])

users_db: List[dict] = []
next_user_id = 1

def get_current_user(auth_username: str) -> dict:
    """Mendapatkan data user berdasarkan username, untuk simulasi otorisasi."""
    for user_data in users_db:
        if user_data['username'] == auth_username:
            return user_data
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials or user not found"
    )

def authorize_admin(auth_username: str):
    """Memastikan user yang mengakses adalah 'admin'. [cite: 20]"""
    user = get_current_user(auth_username)
    if user['role'] != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Only admin can access this resource."
        )
    return user

@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserIn):
    """
    Membuat user baru. Bisa diakses oleh semua. [cite: 19]
    """
    global next_user_id
    
    if any(u['username'] == user_in.username or u['email'] == user_in.email for u in users_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists."
        )

    now = datetime.now()
    new_user_data = user_in.model_dump()
    
    new_user_data.update({
        "id": next_user_id,
        "created_at": now,
        "updated_at": now,
    })
    
    users_db.append(new_user_data)
    next_user_id += 1
    
    user_out = User(**new_user_data) 
    
    return {
        "success": True, 
        "message": "User successfully created", 
        "data": user_out
    }