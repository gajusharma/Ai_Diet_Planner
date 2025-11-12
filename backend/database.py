import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError

from utils.settings import get_settings

mongo_client: AsyncIOMotorClient | None = None

def get_database():
    if mongo_client is None:
        raise RuntimeError("Mongo client is not initialized")
    settings = get_settings()
    return mongo_client[settings.mongo_db_name]


def connect_to_mongo() -> None:
    global mongo_client
    if mongo_client:
        return
    settings = get_settings()
    
    try:
        # Use TLS options supported by PyMongo instead of unsupported ssl_context
        # certifi provides a CA bundle recognized by MongoDB Atlas
        mongo_client = AsyncIOMotorClient(
            settings.mongo_uri,
            tls=True,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=10000  # 10 second connection timeout
        )
        print(f"MongoDB connection initialized with TLS using certifi CA bundle: {certifi.where()}")
    except Exception as e:
        print(f"Failed to initialize MongoDB connection: {e}")
        raise


def close_mongo_connection() -> None:
    global mongo_client
    if mongo_client:
        try:
            mongo_client.close()
        except PyMongoError:
            pass
        finally:
            mongo_client = None
