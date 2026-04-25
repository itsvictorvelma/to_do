from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from database import engine, TodoDatabase

app = FastAPI()

def get_session():
    with Session(engine) as session: 
        yield session

@app.post("/items")
async def create_item(item: TodoDatabase, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@app.get("/items/{item_id}")
async def get_item(item_id: int, session: Session = Depends(get_session)):
    todo = session.get(TodoDatabase, item_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Item not found...")

    return todo

@app.get("/items")
async def get_all_items(session: Session = Depends(get_session)):
    todos = session.exec(select(TodoDatabase)).all()
    return todos

@app.patch("/items/{item_id}")
async def toggle_completed(item_id: int, session: Session = Depends(get_session)):
    todo = session.get(TodoDatabase, item_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Item not found...")

    todo.is_done = not todo.is_done
    
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@app.delete("/items/{item_id}")
async def delete_item(item_id: int, session: Session = Depends(get_session)):
    todo = session.get(TodoDatabase, item_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Item not found")

    session.delete(todo)
    session.commit()

    return {f"Todo #{item_id} has been deleted"}




    