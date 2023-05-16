# app/main.py

from fastapi import FastAPI, Path

app = FastAPI(title="FastAPI, Docker, and Traefik")

inventory = {
    1: {
        'name': 'Milk',
        'price': 4.25,
        'brand': 'Clover',
    }
}


@app.get('/item/{item_id}')
def get_item(item_id: int = Path(None, description='The ID of the item to get', gt=0)):
    return inventory[item_id]
