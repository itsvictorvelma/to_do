from fastapi import FastAPI, HTTPException
from schemas import Todo

app = FastAPI()

items = []

@app.post("/items")
async def create_item(item: Todo):
    item.id = len(items) + 1
    items.append(item)
    return items

@app.get("/items/{item_id}", response_model=Todo)
def get_item(item_id: int) -> Todo:

    if item_id < len(items):
        for item in items:
            if item.id == item_id:
                return item
    else:
        raise HTTPException(status_code=404, detail="Item not found...")

@app.get("/items")
def get_all_items():
    return items

