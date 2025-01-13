# main.py
"""This module provides user-related APIs for user creation and retrieval."""

import logging
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
import models
from database import engine, get_db
from schemas import UserCreateSchema, UserSchema, UserOrderUpdateSchema
from sqlalchemy import func


models.Base.metadata.create_all(engine)

logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.get("/")
def get_index():
    """Handle GET request for the root endpoint."""
    return {"msg": "User service"}


@app.post("/user")
def post_user(request: UserCreateSchema, db: Session = Depends(get_db)):
    """
    Handle POST request to create a new user.

    Args:
        request: UserCreateSchema object containing user data.
        db: Database session dependency.

    Returns:
        None
    """
    user = models.User(name=request.name, orders=request.orders)
    db.add(user)
    db.commit()
    db.refresh(user)


@app.get("/user/{user_id}", response_model=UserSchema)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    Handle GET request to retrieve a user by their ID.

    Args:
        user_id: The ID of the user to retrieve.
        db: Database session dependency.

    Returns:
        UserSchema: A schema representation of the user.

    Raises:
        HTTPException: If the user is not found, returns a 404 error.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/user/{user_id}", response_model=UserSchema)
def user_update_from_order(user_id: int, request: UserOrderUpdateSchema ,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.orders = func.array_append(user.orders, request.order_id)
    db.commit()
    db.refresh(user)
    return user