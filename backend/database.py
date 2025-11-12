import certifi
import ssl
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
        # Create SSL context with proper CA certificates
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        ssl_context.check_hostname = False  # Disable hostname verification for MongoDB Atlas
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        
        mongo_client = AsyncIOMotorClient(
            settings.mongo_uri,
            ssl=True,
            ssl_context=ssl_context,
            tlsAllowInvalidCertificates=False,
            tlsAllowInvalidHostnames=True,  # Allow Atlas hostnames
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=10000  # 10 second connection timeout
        )
        print(f"MongoDB connection initialized with SSL context using certifi: {certifi.where()}")
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
