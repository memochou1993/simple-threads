from fastapi import APIRouter, Request
from pydantic import BaseModel


class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = [
    {"name": "Foo", "price": 50.2},
    {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
]

router = APIRouter(tags=["Item"])


@router.get("/items")
async def listItems(req: Request):
    return {"data": items}


@router.post("/items")
async def createItem(req: Request, item: Item):
    items.append(item)
    return {"data": item}


@router.get("/items/{item_id}")
async def getItem(req: Request, item_id: int):
    return {"data": items[item_id]}


@router.put("/items/{item_id}")
async def updateItem(req: Request, item_id: int, item: Item):
    items[item_id] = item
    return {"data": item}


@router.delete("/items/{item_id}")
async def deleteItem(req: Request, item_id: int):
    del items[item_id]
    return {"data": {}}
