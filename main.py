from database import engine, Todo, User
from schemas import UserCreate, UserPublic, TodoCreate, TodoPublic
from security import hash_password, verify_password, create_access_token
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from security import oauth2_scheme, verify_access_token
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

def get_session():
    with Session(engine) as session: 
        yield session

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    user_id = verify_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Could not validate credentials.")

    user = session.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")

    return user

@app.post("/items", response_model=TodoPublic)
async def create_item(
    item_in: TodoCreate, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
    ):

    if not current_user.id:
        raise HTTPException(status_code=500, detail="User ID is missing.") 

    new_item = Todo(**item_in.model_dump(), user_id=current_user.id)

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
async def get_my_items(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    statement = select(Todo).where(Todo.user_id == current_user.id)
    todos = session.exec(statement).all()
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

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    
    # get user
    user = session.exec(select(User).where(User.username == form_data.username)).first()

    # verify
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # create token
    access_token = create_access_token(data={"sub": str(user.id)})

    # return user "wristband"
    return {"access_token": access_token, "token_type": "bearer"}

    