from bson.objectid import ObjectId

from utils.db.mongo_nosql import MongoNoSQL


class UserService:
    MONGO_COLLECTION_NAME: str = "users"

    @staticmethod
    def create_user(db_client: MongoNoSQL, user: dict) -> dict | None:
        if user_id := db_client.insert(UserService.MONGO_COLLECTION_NAME, user):
            return db_client.search(UserService.MONGO_COLLECTION_NAME, {'_id': ObjectId(user_id)})

    @staticmethod
    def get_user(db_client: MongoNoSQL, api_key: str) -> dict | None:
        if user := db_client.search(UserService.MONGO_COLLECTION_NAME, {'apiKey': api_key}):
            return user

    @staticmethod
    def get_users(db_client: MongoNoSQL) -> list[dict]:
        return db_client.search_all(UserService.MONGO_COLLECTION_NAME, {})

    @staticmethod
    def update_user(db_client: MongoNoSQL, api_key: str, new_user: dict) -> dict | None:
        if new_user := db_client.update(
                UserService.MONGO_COLLECTION_NAME,
                {'apiKey': api_key},
                new_user
        ):
            return new_user

    @staticmethod
    def delete_user(db_client: MongoNoSQL, api_key: str) -> bool:
        return db_client.delete(UserService.MONGO_COLLECTION_NAME, {'apiKey': api_key})

    @staticmethod
    def auth_user(db_client: MongoNoSQL, api_key: str) -> dict | None:
        if auth_user := UserService.get_user(db_client, api_key):
            return auth_user
