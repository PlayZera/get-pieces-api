from fastapi import HTTPException
from app.core.config import settings
from app.services.ollama_service import OllamaService
from app.services.json_db_service import JsonDBService
from app.services.mongo_db_service import MongoDbService
from app.models.product import ProductResponse

#region Construtor
class ProductService:
    def __init__(self):
        self.backend = JsonDBService() if settings.USE_JSON_STORAGE else MongoDbService()

#endregion
    
#region Métodos auxiliares

    def process_product_list(self, products: list) -> ProductResponse:
        processed_products = []
        
        for product in products:
            try:
                # Validação mínima
                if not getattr(product, 'Codigo', None) or not getattr(product, 'NomeProduto', None):
                    continue
                
                # Salva no banco de dados
                saved_product = self.backend.add_or_update_product(product)
                
                # Obtém descrição técnica
                technical_desc = OllamaService.get_technical_description(
                    product.dict(by_alias=True)
                )
                
                product_data = product.dict(by_alias=True)
                product_data["DescricaoTecnica"] = technical_desc
                processed_products.append(product_data)
                
            except Exception as e:
                continue
        
        return ProductResponse(
            success=bool(processed_products),
            data=processed_products,
            message=f"{len(processed_products)} produtos processados"
        )
    
    async def product_exists(self, code: str) -> bool:
        product = await self.backend.get_product_by_code(code)
        
        if product != None:
            return True

    async def get_product_info(self, code: str) -> ProductResponse:

        product = await self.backend.get_product_by_code(code)
        
        if not product:
            return ProductResponse(
                success=False,
                data=None,
                message=f"Produto com código {code} não encontrado"
            )
        
        return ProductResponse(
            success=True,
            data= product,
            message=None
        )
    
    async def get_top_products(self, page:int, itensPerPage:int) -> ProductResponse:

        products = await self.backend.get_top_products(page, itensPerPage)

        if not products:
            return ProductResponse(
                success=False,
                data=None,
                message=f"Produtos da página {page}, não foram carregados"
            )
        
        return ProductResponse(
            success=True,
            data= products,
            message=str(products.__len__())
        )
    
#endregion