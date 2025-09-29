from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from modules.users.schema.schemas import User, UsersListResponse, UserResponse
from .create_user import users_db, get_current_user, authorize_admin

router = APIRouter(tags=["Users"])

@router.get("/users/", response_model=UsersListResponse, status_code=status.HTTP_200_OK)
def read_all_users(auth_username: str = Depends(authorize_admin)):
    """
    Membaca semua data user. Hanya bisa diakses oleh admin. [cite: 20]
    """
    
    users_out = [User(**u) for u in users_db]
    
    return {
        "success": True, 
        "message": f"Successfully retrieved {len(users_out)} users", 
        "data": users_out
    }

@router.get("/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def read_user(user_id: int, auth_username: str):
    """
    Membaca data user berdasarkan ID. Admin bisa baca semua, staff hanya data sendiri. [cite: 21]
    """
    current_user_data = get_current_user(auth_username)

    target_user_data = next((u for u in users_db if u['id'] == user_id), None)
    
    if target_user_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if current_user_data['role'] == 'staff' and current_user_data['id'] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Staff can only read their own data."
        )

    user_out = User(**target_user_data)
    
    return {
        "success": True, 
        "message": f"User ID {user_id} successfully retrieved", 
        "data": user_out
    }