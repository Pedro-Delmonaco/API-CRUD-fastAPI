from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

fake_db = {}

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    fake_db[item.name] = item
    return item 

@app.get("/items/{item_name}", response_model=Item)
def read_item(item_name: str):
    item = fake_db.get(item_name)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_name}", response_model=Item)
def update_item(item_name: str, item: Item):
    if item_name not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    fake_db[item_name] = item
    return item

@app.delete("/items/{item_name}", response_model=Item)
def delete_item(item_name: str):
    item = fake_db.pop(item_name, None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.get("/items/", response_model=List[Item])
def list_items():
    return list(fake_db.values())
