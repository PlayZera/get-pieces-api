from app.db.mongodb import MongoDB
from app.core.logger import logger

async def create_indexes():
    products_collection = MongoDB.get_collection("products")
    await products_collection.create_index("Codigo", unique=True)
    await products_collection.create_index("NomeProduto")
    logger.info("Índices criados com sucesso")