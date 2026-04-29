from database import engine, Todo, User
from schemas import UserCreate, UserPublic, TodoCreate, TodoPublic
from security import hash_password
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select

app = FastAPI()

def get_session():
    with Session(engine) as session: 
        yield session

@app.post("/items", response_model=TodoPublic)
async def create_item(item_in: TodoCreate, session: Session = Depends(get_session)):
    #TEMP UNTIL WE BUILD LOGIN/TOKEN SYSTEM
    new_item = Todo(**item_in.model_dump(), user_id=1)
    session.add(new_item)
    session.commit()
    session.refresh(new_item)
    return new_item

@app.get("/items/{item_id}")
async def get_item(item_id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, item_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Item not found...")

    return todo

@app.get("/items")
async def get_all_items(session: Session = Depends(get_session)):
    todos = session.exec(select(Todo)).all()
    return todos

@app.patch("/items/{item_id}")
async def toggle_completed(item_id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, item_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Item not found...")

    todo.is_done = not todo.is_done
    
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@app.delete("/items/{item_id}")
async def delete_item(item_id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, item_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Item not found")

    session.delete(todo)
    session.commit()

    return {f"Todo #{item_id} has been deleted"}

@app.post("/users/register", response_model=UserPublic)
def register_user(user_in: UserCreate, session: Session = Depends(get_session)):
    
    #check if user already exists

    query = select(User).where(User.username == user_in.username)
    existing_user = session.exec(query).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken.")

    # since our db has unique=True on our usernames, the db would crash if i tried to add a dup
    # we catch that early to prevent any complications. 
    
    hashed_pw = hash_password(user_in.password) # hash user_in password
    
    # save to db
    
    new_user = User(
        username=user_in.username,
        hashed_password=hashed_pw
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
