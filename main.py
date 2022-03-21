from fastapi import HTTPException, status
import imp
from statistics import mode
from fastapi import Depends, FastAPI
from sqlalchemy.orm.session import Session
import models
from database import engine, get_db
from schemas import UserCreateRequest, UserUpdateRequest


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Hello world!"}


@app.get("/user/all")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users


@app.get("/user/{id}")
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.Users).filter(id == models.Users.id)
    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id:{id} does not exists",
        )
    return user


@app.post("/user/create")
def create_user(request: UserCreateRequest, db: Session = Depends(get_db)):
    user = models.Users(**request.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.put("/user/update/{id}")
def update_user(id: int, request: UserUpdateRequest, db: Session = Depends(get_db)):
    user_query = db.query(models.Users).filter(id == models.Users.id)
    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id:{id} does not exists",
        )
    user_query.update(request.dict())
    db.commit()
    db.refresh(user)
    return user


@app.delete("/user/delete/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.Users).filter(id == models.Users.id)
    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id:{id} does not exists",
        )
    user_query.delete(synchronize_session=False)
    db.commit()
    return {"message": f"user with id:{id} deleted successfully"}
