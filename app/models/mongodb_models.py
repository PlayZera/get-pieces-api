from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List, Optional
from bson import ObjectId
from pydantic_core import core_schema

class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, str):
            try:
                ObjectId(v)
                return v
            except:
                raise ValueError("Invalid ObjectId")
        raise ValueError("Must be ObjectId or str")

class ProductInDB(BaseModel):
    id: PyObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    codigo: Optional[int] = Field(alias="Codigo")
    nome_produto: Optional[str] = Field(None, min_length=0, max_length=1000, alias="NomeProduto")
    tipo_material: Optional[str] = Field(None, min_length=0, max_length=5000, alias="TipoMaterial")
    status: Optional[str] = Field(None, min_length=0, max_length=2000, alias="Statis")
    materiais_texto_longo: Optional[str] = Field(None, max_length=5000, alias="Materiais com Texto Longo para Pedido de Compra")
    descricao_tecnica: Optional[str] = Field(None, max_length=5000, alias="DescricaoTecnica")
    criado: Optional[str] = Field(None, min_length=0, max_length=500, alias="criado")
    atualizado: Optional[str] = Field(None, min_length=0, max_length=500, alias="atualizado")
    imageUrls: Optional[List[str]] = []
    categoria: Optional[str] = Field(None, min_length=0, max_length=500, alias="Categoria")
    descricaoBasica: Optional[str] = Field(None, min_length=0, max_length=5000, alias="DescricaoBasica")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        json_encoders={ObjectId: str},
    )

    @field_validator('id', mode='before')
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
    
class ProductToShow(BaseModel):
    codigo: Optional[str] = Field(None, min_length=0, max_length=500)
    nome_produto: Optional[str] = Field(None, min_length=0, max_length=1000)
    status: Optional[str] = Field(None, min_length=0, max_length=2000)
    categoria: Optional[str] = Field(None, min_length=0, max_length=500)
    urlImagem: Optional[str] = Field(None, min_length=0, max_length=2000)