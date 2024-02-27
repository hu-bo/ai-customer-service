from fastapi import FastAPI  
from pydantic import BaseModel  
  
app = FastAPI()  
  
class Item(BaseModel):  
    name: str  
    description: str = None  
  
@app.get("/items/{item_id}", response_model=Item)  
async def read_item(item_id: int, q: str = None):  
    items = {"item1": {"name": "Foo", "description": "A very nice item"},  
             "item2": {"name": "Bar", "description": "Another nice item"}}  
  
    if item_id not in items:  
        return {"item": "Does not exist"}  
  
    item = items[item_id]  
    if q:  
        if q in item["name"]:  
            return {"item": item}  
        else:  
            return {"item": "Not found"}  
    return {"item": item}  
  
@app.post("/items/")  
async def create_item(item: Item):  
    return {"item": item}  
  
if __name__ == "__main__":  
    import uvicorn  
    uvicorn.run(app, host="0.0.0.0", port=8000)