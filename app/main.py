from fastapi import FastAPI, Request
from handlers import get_item, list_items
from mangum import Mangum

app = FastAPI(root_path="/v1")


@app.get("", include_in_schema=False)
@app.get("/")
async def root():
    return {
        "message": "Hello, World!",
    }


@app.get("/items")
async def listItems(req: Request):
    return list_items.handle(req)


@app.get("/items/{item_id}")
async def getItem(req: Request, item_id: int):
    return get_item.handle(req, item_id)


handler = Mangum(app, lifespan="off")
