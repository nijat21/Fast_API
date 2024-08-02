from fastapi import FastAPI, Path, Query, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI() #created the API object


class Item(BaseModel):
    name:str
    price:float
    brand: Optional[str]=None

class UpdateItem(BaseModel):
    name:Optional[str] = None
    price:Optional[float] = None
    brand: Optional[str]=None

inventory = { }

# Path parameters
@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(..., description="The id of the item you'd like to review", gt=0)): #Path allows adding addition details 
    return inventory[item_id]


# "facebook.com/home?redirec=/tim&msg=fail"
# Query parameters
@app.get("/get-by-name")
def get_by_name(*, name: Optional[str] = None, test: int):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    # return {"Data": "Not found!"} 
    raise HTTPException(status_code=404, detail="Item name not found.")           

# Path and query parameters combined
@app.get("/get-by-name/{item_id}")
def get_by_name(*, item_id:int, name: Optional[str] = None, test: int):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    # return {"Data": "Not found!"}            
    raise HTTPException(status_code=404, detail="Item name not found.")           


@app.post("/create-item/{item_id}")
def create_item(item_id:int,item: Item):
    if item_id in inventory:
        # return {"Error":"Item id already exists in inventory"}
        raise HTTPException(status_code=400, detail="Item id already exists in inventory.")           
    
    # inventory[item_id] = {"name":item.name, "price":item.price, "brand":item.brand}  this is a long way to do it
    inventory[item_id] = item # as of BaseModel, it will automatically parse
    return inventory[item_id]


@app.put("/update-item/{item_id}")
def update_item(item_id:int, item:UpdateItem):
    if item_id not in inventory:
        # return {"Error": "Item ID does not exists."}
        raise HTTPException(status_code=404, detail="Item ID does not exists.")           
    
    if item.name != None:
        inventory[item_id].name = item.name
    if item.price != None:
        inventory[item_id].price = item.price
    if item.brand != None:
        inventory[item_id].brand = item.brand

    return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int = Query(...,description="The ID of the item to delete", gt=0)):
    if item_id not in inventory:
        # return {"Error":"Item doesn't exist."}
        raise HTTPException(status_code=404, detail="Item ID does not exists.")           
    
    del inventory[item_id]
    return {"Success":"Item deleted!"}
