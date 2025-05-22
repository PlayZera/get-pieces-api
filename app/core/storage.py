from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.product import ProductItem

class StorageBackend(ABC):
    @abstractmethod
    def get_all_products(self) -> List[ProductItem]:
        pass
    
    @abstractmethod
    def get_product_by_code(self, code: str) -> Optional[ProductItem]:
        pass
    
    @abstractmethod
    def add_or_update_product(self, product: ProductItem) -> List[ProductItem]:
        pass