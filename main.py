from fastapi import FastAPI, HTTPException
from schemas import Todo

app = FastAPI()

items = []
id_counter = 1

@app.post("/items")
async def create_item(item: Todo):
    item.id = id_counter
    items.append(item)
    id_counter + 1
    return item

@app.get("/items/{item_id}", response_model=Todo)
async def get_item(item_id: int) -> Todo:
    for item in items:
        if item.id == item_id:
            return item

    raise HTTPException(status_code=404, detail="Item not found...")

@app.get("/items")
async def get_all_items():
    return items

@app.patch("/items/{item_id}", response_model=Todo)
async def completed(item_id: int) -> Todo:
    for item in items:
        if item.id == item_id:
            item.is_done = True
            return item

    raise HTTPException(status_code=404, detail="Item not found...")

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    for item in items:
        if item.id == item_id:
            items.remove(item)
            return {"detail": f"Todo #{item_id} has been succesfully deleted"}

    raise HTTPException(status_code=404, detail="Item not found...")

    