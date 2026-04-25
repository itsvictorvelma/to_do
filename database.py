from sqlmodel import Field, SQLModel, create_engine

class TodoDatabase(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    is_done: bool = False
    
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(url=sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)