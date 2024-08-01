from fastapi import FastAPI, Path

app = FastAPI() #created the API object

inventory = {
        1: {
            "name": "Milk",
            "price": 3.5,
            "brand": "Regular"
        }
    }

@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(..., description="The id of the item you'd like to review", gt=0, lt=2)): #Path allows adding addition details 
    return inventory[item_id]


# "facebook.com/home?redirec=/tim&msg=fail"
@app.get("/get-by-name")
def get_by_name(name: str):
    for item_id in invetory:
        if inventory[item_id]['name'] == name:
            return inventory[item_id]
    return {"Data": "Not found!"}            
