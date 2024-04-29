from fastapi import FastAPI
from handlers import item_handler
from mangum import Mangum

app = FastAPI(root_path="/api")


@app.get("", include_in_schema=False)
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Hello, World!",
    }


app.include_router(item_handler.router)
handler = Mangum(app, lifespan="off")
