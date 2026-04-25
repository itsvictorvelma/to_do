from pydantic import BaseModel
from typing import Optional

class Todo(BaseModel):
    id: int
    is_done: bool = False
    title: str 
    description: Optional[str] = None

