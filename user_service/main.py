from fastapi import FastAPI, Depends, HTTPException
from database import engine, get_db
import models
from schemas import UserCreateSchema, UserSchema
from sqlalchemy.orm import Session
import logging


models.Base.metadata.create_all(engine)

logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.get("/")
def get_index():
    return {"msg": "User service"}


@app.post("/user")
def post_user(request: UserCreateSchema, db: Session = Depends(get_db)):
    user = models.User(name=request.name, orders=request.orders)
    db.add(user)
    db.commit()
    db.refresh(user)


@app.get("/user/{user_id}", response_model=UserSchema)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user
