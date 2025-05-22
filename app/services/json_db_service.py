import json
from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException
from app.core.config import settings
from app.core.storage import StorageBackend
from app.models.product import ProductItem, ProductItemCreate
import concurrent.futures
from app.core.logger import logger

class JsonDBService(StorageBackend):
    def __init__(self):
        self.json_path = settings.JSON_DB_PATH
        self.json_path.parent.mkdir(parents=True, exist_ok=True)

    def _read_db(self) -> List[dict]:
        try:
            if not self.json_path.exists():
                return []
                
            with open(self.json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao ler banco de dados JSON: {str(e)}"
            )

    def _write_db(self, data: List[dict]):
        try:
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao escrever no banco de dados JSON: {str(e)}"
            )

    def get_all_products(self) -> List[ProductItem]:
        logger.info("Lendo dados do banco json")
        db_data = self._read_db()
        logger.info(f"Banco lido -> {db_data[:2]}...") 

        # Função auxiliar para processar cada item
        def process_item(item):
            try:
                return ProductItem(**item)
            except Exception as e:
                logger.info(f"Erro ao processar item {item.get('Codigo')}: {str(e)}")
                return None

        num_threads = min(50, len(db_data))  
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            results = list(executor.map(process_item, db_data))

        valid_products = [p for p in results if p is not None]
        logger.info(f"Retornando {len(valid_products)} produtos válidos")
        return valid_products

    def get_product_by_code(self, code: str) -> Optional[ProductItem]:
        
        self.db_data = self._read_db()

        logger.info(f"Iniciando processo de busca por código {self.db_data[:2]}")

        for item in self.db_data:
            try:
                productCode = str(item['Codigo'])
                if  productCode == code:
                    logger.info(f"Encontrado item de banco json -> {item} com código {code}")
                    return ProductItem(**item)
            except Exception as ex:
                logger.info(f"Falha ao validar código: {ex} : Item: {item}")
                pass
        return None
    
    def add_or_update_product(self, product: ProductItemCreate) -> List[ProductItem]:
        db_data = self._read_db()
        now = datetime.now().isoformat()
        product_dict = product.dict(by_alias=True)
        
        # Atualiza se existir
        updated = False
        for item in db_data:
            if item['Codigo'] == product.Codigo:
                item.update(product_dict)
                item['updated_at'] = now
                updated = True
                break
        
        if not updated:
            product_dict.update({
                'created_at': now,
                'updated_at': now
            })
            db_data.append(product_dict)
        
        self._write_db(db_data)
        return [ProductItem(**item) for item in db_data]