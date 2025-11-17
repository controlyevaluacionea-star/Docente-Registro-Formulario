import reflex as rx
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import logging

MONGO_URI = "mongodb+srv://ender:ender2024@cluster0.oarsibs.mongodb.net/"
DATABASE_NAME = "enderavila"


def get_db_client():
    try:
        client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
        client.admin.command("ping")
        return client
    except Exception as e:
        logging.exception(f"Error al conectar con MongoDB: {e}")
        return None


def get_docentes_collection():
    client = get_db_client()
    if client:
        db = client[DATABASE_NAME]
        return db["docentes"]
    return None


def get_users_collection():
    client = get_db_client()
    if client:
        db = client[DATABASE_NAME]
        return db["users"]
    return None