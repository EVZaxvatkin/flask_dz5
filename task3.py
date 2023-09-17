from fastapi import FastAPI, HTTPException
from typing import Optional
import uvicorn as uvicorn
from pydantic import BaseModel


app = FastAPI()

users = []

class User(BaseModel):
    id: int
    name: str
    email: str
    password: str

class UserIn(BaseModel):
    name: str
    email: str
    password: str

@app.get("/users/", response_model=list[User])
async def root():
    return users


@app.post("/users/", response_model=list[User])
async def create_user(new_user: UserIn):
    users.append(User(id=len(users)+1, name=new_user.name, email=new_user.email,password=new_user.password))

    return users

@app.put("/users/", response_model=User)
async def edit_user(user_id: int, new_user: UserIn):
    for i in range(0, len(users)):
        if users[i].id == user_id:
            current_user = users[user_id - 1]
            current_user.name = new_user.name
            current_user.email = new_user.email
            current_user.password = new_user.password
            return current_user
        raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/users/", response_model=dict)
async def del_user(user_id: int):
    for i in range(0, len(users)):
        if users[i].id == user_id:
            users.remove(users[i])
            return {"message": "User was deleted"}
    raise HTTPException(status_code=404, detail="Task not found")



if __name__ == "__main__":
    uvicorn.run("task3:app", host="127.0.0.1", port=8000, reload=True)