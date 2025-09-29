from fastapi import APIRouter, HTTPException, status, Depends
from modules.users.schema.schemas import MessageResponse
from .create_user import users_db, authorize_admin

router = APIRouter(tags=["Users"])

@router.delete("/users/{user_id}", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def delete_user(user_id: int, auth_username: str = Depends(authorize_admin)):
    """
    Menghapus data user berdasarkan ID. Hanya bisa diakses oleh admin. [cite: 20]
    """
    user_index = next((i for i, u in enumerate(users_db) if u['id'] == user_id), None)

    if user_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    deleted_user = users_db.pop(user_index)
    
    return {
        "success": True, 
        "message": f"User ID {user_id} successfully deleted", 
        "data": {"id": user_id, "username": deleted_user['username']}
    }