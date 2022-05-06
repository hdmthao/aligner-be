import logging

from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import MONGODB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT, db_name, sentence_pairs_collection_name
from .mongo import db


logger = logging.getLogger(__name__)

async def connect_to_mongo():
    logger.info("Connecting to MongoDB...")
    db.client = AsyncIOMotorClient(str(MONGODB_URL),
                                   maxPoolSize=MAX_CONNECTIONS_COUNT,
                                   minPoolSize=MIN_CONNECTIONS_COUNT)
    await create_indexs()
    logger.info("Successfully connected to the database!")


async def close_mongo_connection():
    logger.info("Closing database connection...")
    db.client.close()
    logger.info("Database connection closed!")

async def create_indexs():
    await db.client[db_name][sentence_pairs_collection_name].create_index([("src_sent_1_tgt_sent_1", 1), ("src_sent", 1), ("tgt_sent", 1)], unique=True)
    await db.client[db_name][sentence_pairs_collection_name].create_index("id", unique=True)
