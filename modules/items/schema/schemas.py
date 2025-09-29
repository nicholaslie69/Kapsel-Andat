from datetime import datetime
from enum import Enum
from typing import Optional, List
import re
from pydantic import BaseModel, Field, EmailStr, ConfigDict

class Role(str, Enum):
    """Nilai enumerasi untuk role pengguna."""
    ADMIN = "admin"
    STAFF = "staff"

PASSWORD_REGEX = (
    r'^(?=.*[a-z])'
    r'(?=.*[A-Z])'
    r'(?=.*\d)'
    r'(?=.*[!@])'
    r'[A-Za-z\d!@]{8,20}$'
)

class UserIn(BaseModel):
    """Skema input untuk membuat atau memperbarui user."""
    username: str = Field(
        min_length=6, 
        max_length=15, 
        pattern=r'^[a-z0-9]+$', 
        title='Username', 
        description='Alfanumerik lowercase (min 6, max 15)',
        example='johndoe123'
    )
    email: EmailStr = Field(
        title='Email',
        example='john.doe@example.com'
    )
    password: str = Field(
        min_length=8, 
        max_length=20, 
        pattern=PASSWORD_REGEX, 
        title='Password', 
        description='Alfanumerik dengan ! dan @ (min 8, max 20, harus ada huruf kapital, huruf kecil, angka, dan karakter khusus)',
        example='Password!1'
    )
    role: Role = Field(
        title='Role',
        example=Role.STAFF
    )
    
    model_config = ConfigDict(extra="forbid")

class User(BaseModel):
    """Skema output untuk data user."""
    id: int = Field(title='Unique Identifier')
    username: str
    email: EmailStr
    role: Role
    created_at: datetime
    updated_at: datetime

class UserResponse(BaseModel):
    success: bool
    message: str
    data: Optional[User]

class UsersListResponse(BaseModel):
    success: bool
    message: str
    data: List[User]

class MessageResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None