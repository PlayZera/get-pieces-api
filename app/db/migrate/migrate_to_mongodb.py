import asyncio
from app.db.mongodb import MongoDB
from app.models.mongodb_models import ProductInDB
from app.services.json_db_service import JsonDBService
from app.models.product import ProductItem
from app.services.product_service import ProductService

async def migrate():
    await MongoDB.connect()
    json_service = JsonDBService()
    mongo_service = ProductService()
    
    products = json_service.get_all_products()  # Seus produtos antigos
    converted = [
        ProductInDB(
            codigo=p.Codigo,
            nome_produto=p.NomeProduto,
            tipo_material=p.TipoMaterial,
            status=p.Status,
            materiais_texto_longo=p.Materiais_com_Texto_Longo_para_Pedido_de_Compra
        ) for p in products
    ]
    
    count = await mongo_service.import_products(converted)
    print(f"Migrados {count} produtos para o MongoDB")

if __name__ == "__main__":
    asyncio.run(migrate())