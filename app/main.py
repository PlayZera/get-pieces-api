from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.indexes import create_indexes
from app.db.mongodb import MongoDB
from app.routers import auth, products, images
from app.core.config import settings
from app.core.logger import logger
import os

app = FastAPI(
    title="API de Produtos",
    description="API para consulta de produtos",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(images.router)

@app.on_event("startup")
async def startup():
    logger.info("Criando diretórios para imagens de produtos")
    os.makedirs(settings.IMAGES_PATH, exist_ok=True)
    await MongoDB.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    logger.info("Fechando conexões")
    await MongoDB.disconnect()
    await create_indexes()