from sqlmodel import Field, SQLModel, create_engine 
from typing import Optional

class Todo(SQLModel, table=True):
    title: str
    user_id: int = Field(foreign_key="user.id")   
    id: int | None = Field(default=None, primary_key=True)
    is_done: bool = False
    

class User(SQLModel, table=True):
    username: str = Field(unique=True, index=True)
    hashed_password: str
    id: Optional[int] = Field(default=None, primary_key=True)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(url=sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)