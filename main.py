from fastapi import FastAPI, HTTPException
from schemas import Todo

app = FastAPI()

items = []

@app.post("/items")
async def create_item(item: Todo):
    items.append(item)
    return items

@app.get("/items/{item_id}", response_model=Todo)
def get_item(item_id: int) -> Todo:

    if item_id < len(items):
        return items[item_id]

    else:
        raise HTTPException(status_code=404, detail="Item not found...")

