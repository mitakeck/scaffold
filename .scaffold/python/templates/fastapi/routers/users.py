"""
User management endpoints for {{name}}
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import structlog

from ..database import get_db
from ..models import User, UserCreate, UserUpdate, UserResponse, UserList
{{#if auth}}
from ..auth import get_current_user, get_password_hash
{{/if}}

router = APIRouter()
logger = structlog.get_logger()


@router.get("/", response_model=UserList)
async def get_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    {{#if database}}
    db: AsyncSession = Depends(get_db),
    {{/if}}
    {{#if auth}}
    current_user: User = Depends(get_current_user),
    {{/if}}
):
    """Get paginated list of users."""
    {{#if database}}
    # Calculate offset
    offset = (page - 1) * size
    
    # Get users with pagination
    users_query = select(User).offset(offset).limit(size)
    users_result = await db.execute(users_query)
    users = users_result.scalars().all()
    
    # Get total count
    count_query = select(func.count(User.id))
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    return UserList(
        users=[UserResponse.from_orm(user) for user in users],
        total=total,
        page=page,
        size=size
    )
    {{else}}
    # Mock data when no database is configured
    mock_users = [
        UserResponse(
            id=1,
            email="user@example.com",
            full_name="Example User",
            is_active=True,
            created_at=datetime.utcnow(),
        )
    ]
    return UserList(
        users=mock_users,
        total=1,
        page=page,
        size=size
    )
    {{/if}}


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreate,
    {{#if database}}
    db: AsyncSession = Depends(get_db),
    {{/if}}
    {{#if auth}}
    current_user: User = Depends(get_current_user),
    {{/if}}
):
    """Create a new user."""
    {{#if database}}
    # Check if user already exists
    existing_user_query = select(User).where(User.email == user_data.email)
    existing_user_result = await db.execute(existing_user_query)
    existing_user = existing_user_result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
    
    # Create new user
    user_dict = user_data.model_dump()
    {{#if auth}}
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    {{/if}}
    
    user = User(**user_dict)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    logger.info("User created", user_id=user.id, email=user.email)
    return UserResponse.from_orm(user)
    {{else}}
    # Mock response when no database is configured
    logger.info("Mock user creation", email=user_data.email)
    return UserResponse(
        id=1,
        email=user_data.email,
        full_name=user_data.full_name,
        is_active=user_data.is_active,
        created_at=datetime.utcnow(),
    )
    {{/if}}


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    {{#if database}}
    db: AsyncSession = Depends(get_db),
    {{/if}}
    {{#if auth}}
    current_user: User = Depends(get_current_user),
    {{/if}}
):
    """Get user by ID."""
    {{#if database}}
    user_query = select(User).where(User.id == user_id)
    user_result = await db.execute(user_query)
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse.from_orm(user)
    {{else}}
    # Mock response when no database is configured
    if user_id != 1:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=1,
        email="user@example.com",
        full_name="Example User",
        is_active=True,
        created_at=datetime.utcnow(),
    )
    {{/if}}


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    {{#if database}}
    db: AsyncSession = Depends(get_db),
    {{/if}}
    {{#if auth}}
    current_user: User = Depends(get_current_user),
    {{/if}}
):
    """Update user by ID."""
    {{#if database}}
    user_query = select(User).where(User.id == user_id)
    user_result = await db.execute(user_query)
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user fields
    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    
    await db.commit()
    await db.refresh(user)
    
    logger.info("User updated", user_id=user.id, email=user.email)
    return UserResponse.from_orm(user)
    {{else}}
    # Mock response when no database is configured
    if user_id != 1:
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info("Mock user update", user_id=user_id)
    return UserResponse(
        id=1,
        email="user@example.com",
        full_name="Updated User",
        is_active=True,
        created_at=datetime.utcnow(),
    )
    {{/if}}


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    {{#if database}}
    db: AsyncSession = Depends(get_db),
    {{/if}}
    {{#if auth}}
    current_user: User = Depends(get_current_user),
    {{/if}}
):
    """Delete user by ID."""
    {{#if database}}
    user_query = select(User).where(User.id == user_id)
    user_result = await db.execute(user_query)
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await db.delete(user)
    await db.commit()
    
    logger.info("User deleted", user_id=user_id)
    return {"message": "User deleted successfully"}
    {{else}}
    # Mock response when no database is configured
    if user_id != 1:
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info("Mock user deletion", user_id=user_id)
    return {"message": "User deleted successfully"}
    {{/if}}