from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.core.logger import logger

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

    @classmethod
    async def connect(cls):
        cls.client = AsyncIOMotorClient(settings.MONGODB_URI)
        cls.db = cls.client[settings.MONGODB_NAME]
        logger.info("Conectado ao MongoDB")

    @classmethod
    async def disconnect(cls):
        cls.client.close()
        logger.info("Desconectado do MongoDB")

    @classmethod
    def get_collection(cls, collection_name: str):
        return cls.db[collection_name]
    
    async def create_schema():
        await MongoDB.db.command({
            "collMod": "products",
            "validator": {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["Codigo", "NomeProduto"],
                    "properties": {
                        "Codigo": {
                            "bsonType": "string",
                            "minLength": 1,
                            "maxLength": 50
                        },
                        "NomeProduto": {
                            "bsonType": "string",
                            "minLength": 1,
                            "maxLength": 100
                        }
                    }
                }
            }
        })