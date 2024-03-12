from pydantic import BaseModel
from uuid import UUID


class Task(BaseModel):
    id: UUID
    user: str
    text: str
    created_at: str
    updated_at: str
    checked: bool
    important: bool
