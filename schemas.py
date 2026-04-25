from pydantic import BaseModel
from typing import Optional

class Todo(BaseModel):
    id: int
    title: str 
    is_done: bool = False

