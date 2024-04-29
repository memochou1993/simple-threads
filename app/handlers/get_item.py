from fastapi import Request


def handle(request: Request, item_id: int):
    return {
        "request_method": request.method,
        "root_path": request.scope["root_path"],
        "path": request.scope["path"],
    }
