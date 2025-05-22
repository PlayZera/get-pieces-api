import os
import shutil
from typing import Optional
from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.core.config import settings
from app.models.product import ProductResponse, ImageRequest
from app.services.product_service import ProductService
from app.core.logger import logger
from returns.result import Result
from returns.pipeline import flow

class ImageService:
    #region Construtor
    def __init__(self, requisicao:ImageRequest):
        self.imagePath = settings.IMAGES_PATH
        self.codigoProduto = requisicao.code
        self.imagemEnviada = requisicao.file
    #endregion
    
    #region Pipelines
    async def PipelineUploadImage(self):
        return await flow(await self.ValidarImagem(),
                          lambda contexto: self.AdicionarDocumento(contexto))
    
    def PipelineShowImage(self):
        return self.MostrarImagem()

    #endregion

    #region Métodos auxiliares

    async def ValidarImagem(self) -> Result[any, HTTPException]:
        service = ProductService()

        if not service.product_exists(self.codigoProduto):
            raise HTTPException(status_code=404, detail="Produto não encontrado, informe o código de um produto válido")
        
        if not self.imagemEnviada.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Arquivo não é uma imagem")

    async def AdicionarDocumento(self) -> Result[ProductResponse, HTTPException]:
        try:
            nomeArquivo = f"{self.codigoProduto}.jpg"
            with open(os.path.join(self.imagemEnviada, nomeArquivo), "wb") as buffer:
                shutil.copyfileobj(self.imagemEnviada, buffer)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao salvar imagem: {str(e)}")
        
        return ProductResponse(
            message = f"Documento enviado com sucesso: {nomeArquivo}",
            success= True)

    async def MostrarImagem(self) -> Result[FileResponse, HTTPException]:
        diretorioImagem = os.path.join(settings.IMAGES_PATH, f"{self.codigoProduto}.jpg")

        if not os.path.exists(diretorioImagem):
            raise HTTPException(status_code=404, detail="Imagem não encontrada")
    
        return FileResponse(diretorioImagem)
    
    #endregion


    async def UploadImage(self) -> Optional[ProductResponse]:
        logger.info(f"Iniciando fluxo de upload de imagem.")

        result = await self.PipelineUploadImage()
        return result
    
    def ShowImage(self) -> Optional[FileResponse]:
        logger.info(f"Iniciando fluxo de recuperação de imagens.")

        result = self.PipelineShowImage()
        return result
