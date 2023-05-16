# app/main.py

from fastapi import FastAPI, Path, HTTPException, status
from typing import Optional
from pydantic import BaseModel


app = FastAPI(title="FastAPI, Docker, and Traefik")

# Base Model


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


inventory1 = {
    1: {
        'name': 'Milk',
        'price': 4.25,
        'brand': 'Clover',
    },
    2: {
        'name': 'Bread',
        'price': 2.50,
        'brand': 'Wonder',
    },
}

inventory2 = {
    1: Item(name='Milk', price=4.25, brand='Clover'),
    2: Item(name='Bread', price=2.50, brand='Wonder'),
    3: Item(name='Water', price=1.25, brand='Dasani'),
}

# path parameters


@app.get('/item1/{item_id}')
def get_item(item_id: int = Path(None, description='The ID of the item to get', gt=0)):
    return inventory1[item_id]

# query parameters


@app.get('/item-by-name')
def get_item(name: str):
    for item in inventory1.values():
        if item['name'] == name:
            return item
    return {'Data': 'Not Found'}


# optional query parameters
@app.get('/item-by-price')
def get_item(price: Optional[float] = None, brand: Optional[str] = None):
    for item in inventory1.values():
        if item['price'] == price:
            return item
        if item['brand'] == brand:
            return item
    return {'Data': 'Not Found'}

# request body


@app.post('/item-create')
def create_item(item: Item):
    item_id = len(inventory2) + 1
    inventory2[item_id] = item
    return inventory2[item_id]


@app.get('/item2/{item_name}')
def get_item(item_name: str = Path(None, description='The name of the item to get')):
    for item in inventory2.values():
        if item.name == item_name:
            return item
    return {'Data': 'Not Found'}

# update item


@app.put('/item-update/{item_id}')
def update_item(item_id: int, item: UpdateItem):
    if item_id in inventory2:
        # to prevent overwriting the existing data with None values
        if item.name != None:
            inventory2[item_id].name = item.name
        if item.price != None:
            inventory2[item_id].price = item.price
        if item.brand != None:
            inventory2[item_id].brand = item.brand
        return inventory2[item_id]
    return {'Error': 'Item does not exist'}

# delete item


@app.delete('/item-delete/{item_id}')
def delete_item(item_id: int):
    if item_id in inventory2:
        del inventory2[item_id]
        return {'Message': 'Item deleted successfully'}
    # raise an error if the item does not exist
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Item does not exist')
