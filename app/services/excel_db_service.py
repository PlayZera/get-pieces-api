import pandas as pd
import os
from fastapi import HTTPException
from ..core.config import settings
from ..services.ollama_service import OllamaService

class ExcelDBService:
    @staticmethod
    def find_product(code: int) -> dict:
        try:
            df_produtos = pd.read_excel(settings.EXCEL_FILE)
            product = df_produtos[df_produtos['codigo'] == code].to_dict('records')
            if not product:
                return None
            
            image_path = os.path.join(settings.IMAGES_DIR, f"{code}.jpg")
            if os.path.exists(image_path):
                product[0]['image_url'] = f"/images/{code}.jpg"
            else:
                product[0]['image_url'] = None
                
            return product[0]
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao acessar dados do produto: {str(e)}"
            )

    @staticmethod
    def get_product_info(product_code: int):
        product = ExcelDBService.find_product(product_code)
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Produto com código {product_code} não encontrado"
            )
        
        technical_desc = OllamaService.get_technical_description(product)
        
        return {
            "product_code": product_code,
            "product_info": {k: v for k, v in product.items() if k != 'image_url'},
            "technical_description": technical_desc,
            "image_url": product.get('image_url')
        }