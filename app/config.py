import os

from dotenv import load_dotenv

load_dotenv()

AWS_VPC_ID = os.getenv("AWS_VPC_ID")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")

DYNAMODB_ENDPOINT_URL = os.getenv("DYNAMODB_ENDPOINT_URL")
DYNAMODB_USER_TABLE_NAME = os.getenv("DYNAMODB_USER_TABLE_NAME")
DYNAMODB_THREAD_TABLE_NAME = os.getenv("DYNAMODB_THREAD_TABLE_NAME")
