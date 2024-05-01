from uuid import uuid4

import boto3
import config
from auth.api_key_header import api_key_header
from boto3.dynamodb.conditions import Attr
from fastapi import APIRouter, Request, Response, Security, status
from models.user import User
from requests.user_store_request import UserStoreRequest
from requests.user_update_request import UserUpdateRequest

session = boto3.Session(region_name=config.AWS_REGION_NAME)
dynamodb = session.resource("dynamodb", endpoint_url=config.DYNAMODB_ENDPOINT_URL)
table = dynamodb.Table(config.DYNAMODB_USER_TABLE_NAME)

router = APIRouter(tags=["User"], prefix="/users")


@router.get("")
async def list_users(req: Request, resp: Response, api_key: str = Security(api_key_header)):
    response = table.scan()
    records = response.get("Items", [])

    return {"data": records}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(req: Request, resp: Response, payload: UserStoreRequest, api_key: str = Security(api_key_header)):
    user_id = str(uuid4())
    user = User(user_id=user_id, **payload.model_dump())

    response = table.scan(FilterExpression=Attr("email").eq(user.email))
    existing_records = response.get("Items", [])
    if existing_records:
        resp.status_code = status.HTTP_409_CONFLICT
        return {"error": "Email already exists"}

    table.put_item(Item=user.model_dump())

    return {"data": user}


@router.get("/{user_id}")
async def get_user(req: Request, resp: Response, user_id: str, api_key: str = Security(api_key_header)):
    response = table.get_item(Key={"user_id": user_id})
    record = response.get("Item", None)
    if record is None:
        resp.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "User not found"}

    return {"data": record}


@router.put("/{user_id}")
async def update_user(
    req: Request, resp: Response, user_id: str, payload: UserUpdateRequest, api_key: str = Security(api_key_header)
):
    response = table.get_item(Key={"user_id": user_id})
    record = response.get("Item", None)
    if record is None:
        resp.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "User not found"}

    user = User(**{**record, **payload.model_dump()})
    table.put_item(Item=user.model_dump())

    return {"data": user}


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(req: Request, resp: Response, user_id: str, api_key: str = Security(api_key_header)):
    response = table.get_item(Key={"user_id": user_id})
    record = response.get("Item", None)
    if record is None:
        resp.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "User not found"}

    table.delete_item(Key={"user_id": user_id})

    return None
