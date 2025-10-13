from motor.motor_asyncio import AsyncIOMotorClient
import logging

from config import MONGO_URI, MONGO_DB_NAME

logger = logging.getLogger("smart-task-planner")

client: AsyncIOMotorClient = None
db = None


async def connect_to_mongo():
    """
    Connects to MongoDB Atlas during application startup and sets up
    the global client and database object for use in routes.
    """
    global client, db
    try:
        if not MONGO_URI or not MONGO_DB_NAME:
            logger.error("MongoDB URI or DB Name is missing in configuration.")
            raise ValueError(
                "MongoDB configuration missing. Cannot start DB connection."
            )
        client = AsyncIOMotorClient(MONGO_URI)
        db = client[MONGO_DB_NAME]

        await db.command("ping")
        logger.info("Connected successfully to MongoDB Atlas and ping successful.")

    except Exception as e:
        logger.error("Could not connect to MongoDB Atlas: %s", e)
        raise RuntimeError("Failed to connect to MongoDB.") from e


async def close_mongo_connection():
    """Closes the MongoDB connection during application shutdown."""
    global client
    if client:
        client.close()
        logger.info("MongoDB connection closed.")


def get_plan_collection():
    """Returns the MongoDB collection where 'plans' are stored."""
    global db

    if db is not None:
        return db.get_collection("plans")
    raise RuntimeError(
        "Database connection failed during runtime. MongoDB client is not initialized."
    )
