import boto3
import os
import json
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()  

SECRET_NAME = "dev/kalosai/database_url"
REGION = os.getenv("AWS_REGION", "ap-south-1")

@lru_cache()
def _load_secrets():
    session_kwargs = {
        "region_name": REGION,
    }

    # Use local credentials from .env if present
    if os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY"):
        session_kwargs["aws_access_key_id"] = os.getenv("AWS_ACCESS_KEY_ID")
        session_kwargs["aws_secret_access_key"] = os.getenv("AWS_SECRET_ACCESS_KEY")

    client = boto3.client("secretsmanager", **session_kwargs)
    response = client.get_secret_value(SecretId=SECRET_NAME)
    return json.loads(response["SecretString"])

@lru_cache()
def get_database_url():
    return _load_secrets()["DATABASE_URL"]

@lru_cache()
def get_google_client_id():
    return _load_secrets()["GOOGLE_CLIENT_ID"]