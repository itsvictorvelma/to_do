from sqlmodel import Field, SQLModel, create_engine 
from typing import Optional

class Todo(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id")   
    id: int | None = Field(default=None, primary_key=True)
    title: str
    is_done: bool = False
    

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    salt: str


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(url=sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)