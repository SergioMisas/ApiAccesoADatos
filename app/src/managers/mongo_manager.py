from pymongo import MongoClient
from src.models.user import User
from src.models.task import Task
from uuid import UUID


class MongoManager:
    def __init__(self, us, pwd):
        self.client = MongoClient(
            f"mongodb://{us}:{pwd}@mongo:27017", uuidRepresentation="standard"
        )
        self.database = self.client["example"]

    def get_users(self) -> list[User]:
        return list(self.database["users"].find())

    def create_user(self, user: User) -> User | None:
        if self.database["users"].find_one({"id": user.id}):
            return None
        self.database["users"].insert_one(user.model_dump())
        return user

    def update_user(self, user: User) -> User | None:
        if not self.database["users"].find_one({"id": user.id}):
            return None
        self.database["users"].update_one({"id": user.id}, {"$set": user.model_dump()})
        return user

    def delete_user(self, id: str) -> User | None:
        user = self.database["users"].find_one({"id": id})
        if not user:
            return None
        tasks = self.database["tasks"].find({"user": id})
        for task in tasks:
            self.database["tasks"].delete_one({"id": task["id"]})
        self.database["users"].delete_one({"id": id})
        return user

    def get_tasks(self) -> list[Task]:
        return list(self.database["tasks"].find())

    def get_tasks_by_user(self, user: str) -> list[Task]:
        return list(self.database["tasks"].find({"user": user}))

    def create_task(self, task: Task) -> Task | None:
        if self.database["tasks"].find_one({"id": task.id}):
            return None
        if not self.database["users"].find_one({"id": task.user}):
            return None
        self.database["tasks"].insert_one(task.model_dump())
        return task

    def update_task(self, task: Task) -> Task | None:
        if not self.database["tasks"].find_one({"id": task.id}):
            return None
        if not self.database["users"].find_one({"id": task.user}):
            return None
        self.database["tasks"].update_one({"id": task.id}, {"$set": task.model_dump()})
        return task

    def delete_task(self, id: UUID) -> Task | None:
        task = self.database["tasks"].find_one({"id": id})
        if not task:
            return None
        self.database["tasks"].delete_one({"id": id})
        return task
