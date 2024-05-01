from fastapi import FastAPI, Request
from handlers import user_handler
from mangum import Mangum

app = FastAPI(root_path="/production", title="Simple Threads API")


@app.get("", include_in_schema=False)
@app.get("/", tags=["Root"])
async def root(req: Request):
    return {
        "message": "Hello, World!",
        "root_path": req.scope.get("root_path"),
    }


app.include_router(user_handler.router, prefix="/api")
handler = Mangum(app, lifespan="off")
