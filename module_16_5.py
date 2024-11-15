from mailbox import Message

from fastapi import FastAPI, status, Body, HTTPException, Request, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates
from typing import Annotated

app = FastAPI()
templates = Jinja2Templates(directory='templates')

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/")
def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users":users})


@app.get('/user/{user_id}')
async def get_users(
    request: Request,
    user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')]
) -> HTMLResponse:
    for user in users:
        if int(user.id) == user_id:
            return templates.TemplateResponse('users.html', {'request': request, 'user': user})
    raise HTTPException(status_code=404, detail='User was not found')

@app.post("/user/{username}/{age}", response_model=User)
async def create_user(username: str, age: int):
    user_id = max(users, key=lambda x: int(x.id)).id + 1 if users else 1
        #(users[-1].id + 1) if users else 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def update_user(user_id: int, username:str, age:int) -> str:
    try:
        for user in users:
            if user.id == user_id:
                user.username = username
                user.age = age
                return user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}", response_model=User)
async def delete_user(user_id: int):
    for user in users:
        if user.id  == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")

