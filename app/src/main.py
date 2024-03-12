import os

from dotenv import load_dotenv
from fastapi import FastAPI
from src.models.user import User
from src.models.task import Task
from uuid import UUID

from src.managers.mongo_manager import MongoManager


app = FastAPI()

load_dotenv()
db_election = os.getenv("DB")

if db_election == "mongo":
    manager = MongoManager(os.getenv("DBUSER"), os.getenv("DBPWD"))
elif db_election == "mariadb":
    pass


@app.get("/")
async def pong():
    return {"message": "Hello World"}


@app.get("/users")
async def get_users() -> list[User]:
    return manager.get_users()


@app.post("/users")
async def create_user(user: User) -> User:
    ret = manager.create_user(user)
    if ret:
        return ret
    else:
        return {"message": "User already exists"}


@app.put("/users")
async def update_user(user: User) -> User:
    ret = manager.update_user(user)
    if ret:
        return ret
    else:
        return {"message": "User not found"}


@app.delete("/users/{id}")
async def delete_user(id: str) -> User:
    ret = manager.delete_user(id)
    if ret:
        return ret
    else:
        return {"message": "User not found"}


@app.get("/tasks")
async def get_tasks() -> list[Task]:
    return manager.get_tasks()


@app.get("/tasks/{user}")
async def get_tasks_by_user(user: str) -> list[Task]:
    return manager.get_tasks_by_user(user)


@app.post("/tasks")
async def create_task(task: Task) -> Task:
    ret = manager.create_task(task)
    if ret:
        return ret
    else:
        return {"message": "Task already exists OR user not found"}


@app.put("/tasks")
async def update_task(task: Task) -> Task:
    ret = manager.update_task(task)
    if ret:
        return ret
    else:
        return {"message": "Task not found"}


@app.delete("/tasks/{id}")
async def delete_task(id: UUID) -> Task:
    ret = manager.delete_task(id)
    if ret:
        return ret
    else:
        return {"message": "Task not found"}
