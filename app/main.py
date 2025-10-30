from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.db.indexes import create_indexes
from app.db.mongodb import MongoDB
from app.routers import auth, products, images
from app.core.config import settings
from app.core.logger import logger
import os
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI(
    title="API de Produtos",
    description="API para consulta de produtos",
    version="1.0.0"
)

# Middleware para debug de CORS
class CORSDebugMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        logger.info(f"Origin: {request.headers.get('origin')}")
        logger.info(f"Headers: {dict(request.headers)}")
        
        response = await call_next(request)
        
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response headers: {dict(response.headers)}")
        
        return response

# Adicionar middleware de debug apenas se não estiver em produção
if not settings.PRODUCTION:
    app.add_middleware(CORSDebugMiddleware)

# Configuração CORS - deve vir ANTES do HTTPS redirect
# Em produção, especifique domínios específicos para maior segurança
allowed_origins = ["*"] if not settings.PRODUCTION else [
    "https://getpiecesaifront-production.up.railway.app",  # Substitua pelo seu domínio do frontend
    "http://localhost:3000",  # Para desenvolvimento local
    "http://localhost:5173",  # Para Vite
    "http://localhost:8080"   # Para outros servidores locais
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,  # False quando allow_origins=["*"]
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600  # Cache preflight por 1 hora
)

# HTTPS redirect apenas em produção
if settings.PRODUCTION:
    logger.warning("Forçando uso de requisições HTTPS")
    app.add_middleware(HTTPSRedirectMiddleware)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(images.router)

# Endpoint de healthcheck para testar CORS
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "API is running"}

@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    return {"message": "OK"}

@app.on_event("startup")
async def startup():
    logger.info("Criando diretórios para imagens de produtos")
    os.makedirs(settings.IMAGES_PATH, exist_ok=True)
    await MongoDB.connect()
    await create_indexes()

@app.on_event("shutdown")
async def shutdown_db_client():
    logger.info("Fechando conexões")
    await MongoDB.disconnect()