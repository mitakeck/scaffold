"""
Data models for {{name}}
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
{{#if database}}
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    """User database model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    {{#if auth}}
    hashed_password = Column(String(255), nullable=False)
    {{/if}}
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
{{/if}}


# Pydantic models for API
class UserBase(BaseModel):
    """Base user model."""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    is_active: bool = True


class UserCreate(UserBase):
    """User creation model."""
    {{#if auth}}
    password: str = Field(..., min_length=8, max_length=128)
    {{/if}}


class UserUpdate(BaseModel):
    """User update model."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """User response model."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserList(BaseModel):
    """User list response model."""
    users: list[UserResponse]
    total: int
    page: int
    size: int


{{#if auth}}
class Token(BaseModel):
    """Authentication token model."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data model."""
    email: Optional[str] = None


class UserLogin(BaseModel):
    """User login model."""
    email: EmailStr
    password: str
{{/if}}


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    version: str
    timestamp: datetime
    {{#if database}}
    database: str
    {{/if}}


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)