from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    email: str

class User(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str
    role: str
    created_at: datetime

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    hashed_password: Optional[str] = None
    role: Optional[str] = None

fake_db: List[User] = []
next_id = 1

def get_db():
    return fake_db

@app.get("/")
async def root():
    return {"message": "Welcome to Distributed Threat Intelligence System", "docs": "/docs"}

@app.get("/users", response_model=List[User])
async def get_users(db: List[User] = Depends(get_db)):
    return db

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, db: List[User] = Depends(get_db)):
    for user in db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/users", response_model=User, status_code=201)
async def create_user(user_data: UserCreate, db: List[User] = Depends(get_db)):
    global next_id
    new_user = User(
        id=next_id,
        username=user_data.username,
        email=user_data.email,
        hashed_password="random123",
        role="client",
        created_at=datetime.now()
    )

    db.append(new_user)
    next_id += 1
    return new_user

@app.put("/users/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: List[User] = Depends(get_db)
):
    for i, user in enumerate(db):
        if user.id == user_id:
            update_data = user_data.dict(exclude_unset=True)
            updated_user = user.copy(update=update_data)
            db[i] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: List[User] = Depends(get_db)):
    for i, user in enumerate(db):
        if user.id == user_id:
            deleted_user = db.pop(i)
            return {"message": f"User '{deleted_user.username}' deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
