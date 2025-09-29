from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from modules.users.schema.schemas import User, UserIn, UserResponse
from .create_user import users_db, authorize_admin

router = APIRouter(tags=["Users"])

@router.put("/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id: int, updated_user: UserIn, auth_username: str = Depends(authorize_admin)):
    """
    Memperbarui data user berdasarkan ID. Hanya bisa diakses oleh admin. [cite: 20]
    """
    user_index = next((i for i, u in enumerate(users_db) if u['id'] == user_id), None)
    
    if user_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    for i, user in enumerate(users_db):
        if i != user_index and (user['username'] == updated_user.username or user['email'] == updated_user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists."
            )
    
    user_data = users_db[user_index]
    
    new_data = updated_user.model_dump()
    new_data['id'] = user_data['id']
    new_data['created_at'] = user_data['created_at']
    new_data['updated_at'] = datetime.now()

    users_db[user_index] = new_data
    
    user_out = User(**new_data)
    
    return {
        "success": True, 
        "message": f"User ID {user_id} successfully updated", 
        "data": user_out
    }