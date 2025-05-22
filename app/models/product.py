from fastapi import UploadFile
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Union
from datetime import datetime

class ProductItemBase(BaseModel):
    Codigo: Optional[str] = Field(None, min_length=1, max_length=1000)
    NomeProduto: Optional[str] = Field(None, min_length=1, max_length=1000)
    TipoMaterial: Optional[str] = Field(None, min_length=1, max_length=1000)
    Status: Optional[str] = Field(None, min_length=1, max_length=1000)
    DescricaoTecnica: Optional[str] = Field(None, min_length=1, max_length=10000)

    # Validadores para converter qualquer valor para string
    @validator('Codigo', 'NomeProduto', 'TipoMaterial', 'Status', pre=True)
    def convert_to_string(cls, value):
        if value is None:
            return None
        return str(value)

class ProductItemCreate(ProductItemBase):
    Materiais_com_Texto_Longo_para_Pedido_de_Compra: Optional[str] = Field(
        None, 
        max_length=500,
        alias="Materiais com Texto Longo para Pedido de Compra"
    )

class ProductItem(ProductItemCreate):
    created_at: Optional[datetime] = Field(None, min_length=1, max_length=100)
    updated_at: Optional[datetime] = Field(None, min_length=1, max_length=100)

    class Config:
        extra = "allow"
        validate_by_name = True

class ProductListRequest(BaseModel):
    products: List[ProductItemCreate]

class ProductResponse(BaseModel):
    success: bool
    data: object
    message: Optional[str] = None

class ImageRequest(BaseModel):
    code: Optional[str] = Field(None, min_length=0, max_length=100)
    file: Optional[UploadFile] = Field(None)