from bson.objectid import ObjectId
from pymongo import AsyncMongoClient


async def insert_into_collection(
    documents: list[dict[str, str | list[str]]],
    client: AsyncMongoClient,
    dbname: str,
    collection_name: str,
) -> list[ObjectId]:
    db = client[dbname]
    collection = db[collection_name]
    result = await collection.insert_many(documents=documents)

    return result.inserted_ids
