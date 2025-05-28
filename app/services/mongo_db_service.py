from datetime import datetime
from typing import Optional
from fastapi import HTTPException
from app.core.logger import logger
from app.core.config import settings
from app.db.mongodb import MongoDB
from app.models.mongodb_models import ProductInDB, ProductToShow
from app.services.ollama_service import OllamaService
from app.services.gemini_service import GeminiService
from bson import ObjectId
from returns.result import Result
from app.services.google_pse_service import GooglePseService
from app.utils.google_pse_utils import GooglePseUtils


class MongoDbService:

    #region construtor
    def __init__(self):
        self.mongoDb = MongoDB.get_collection('products_now')
        logger.info(f"Coleção selecionada: {self.mongoDb.name}")
    #endregion

    #region métodos auxiliares
    
    async def BuscarRegistroEmBanco(self, code:str) -> Result[ProductInDB, HTTPException]:

        try:
            product:ProductInDB = await self.mongoDb.find_one({"Codigo": int(code)})
    
            if product is None:
                logger.error(f"Não encontrado produto com o código {code}")
                raise HTTPException(detail = f"Não encontrado produto com o código {code}",
                                    status_code = 404)
            
            product = ProductInDB(**product)

            logger.info(f"Registro encontrado com o id: {product.id}, nome: {product.nome_produto}, atualizado: {product.atualizado}")

            return product
        
        except Exception as ex:
            logger.error(f"Falha ao busca registro em banco, código: {code}, falha: {ex}")
            raise HTTPException(detail=f"Falha ao buscar produto com o código: {code} falha: {ex}",
                                status_code=500)
        
    async def GerarDescricaoTecnica(self, produto:ProductInDB) -> Result[ProductInDB, HTTPException]:
        try:
            logger.debug(f"Descrição técnica retornada do banco: {produto.descricao_tecnica}")

            if produto.descricao_tecnica is None:
                
                logger.info(f"Não foi encontrada descrição técnica para o produto com o código: {produto.codigo}")

                quantidadeResultados = 5

                listaDeResultadosDeBusca = GooglePseService.search_google_pse(api_key=settings.GOOGLE_PSE_KEY,
                                                                              search_engine_id=settings.GOOGLE_PSE_ID,
                                                                              query=produto.nome_produto,
                                                                              count=quantidadeResultados)

                produto.descricao_tecnica = str(OllamaService.get_technical_description(produto.model_dump(by_alias=True,), listaDeResultadosDeBusca))

            else:
                logger.info(f"O Produto já possui descrição técnica, código: {produto.codigo}")

            return produto

        except Exception as ex:
                logger.error(f"Falha ao gerar descrição do produto com o código: {produto.codigo}, falha: {ex}")
                raise HTTPException(detail=f"Falha ao buscar produto com o código: {produto.codigo} falha: {ex}",
                                    status_code=500)

    async def GerarDescricaoTecnicaComGemini(self, produto:ProductInDB) -> Result[ProductInDB, HTTPException]:
        try:
            logger.debug(f"Descrição técnica retornada do banco: {produto.descricao_tecnica}")

            if produto.descricao_tecnica is None:
                logger.info(f"Não foi encontrada descrição técnica para o produto com o código: {produto.codigo}")
                quantidadeResultados = 5
                listaDeResultadosDeBusca = GooglePseService.search_google_pse(api_key=settings.GOOGLE_PSE_KEY,
                                                                              search_engine_id=settings.GOOGLE_PSE_ID,
                                                                              query=produto.nome_produto,
                                                                              count=quantidadeResultados)
                
                produto.descricao_tecnica = str(GeminiService.get_technical_description(produto.model_dump(by_alias=True,), listaDeResultadosDeBusca))

            else:
                logger.info(f"O Produto já possui descrição técnica, código: {produto.codigo}")

            return produto
        
        except Exception as ex:
                logger.error(f"Falha ao gerar descrição do produto com o código: {produto.codigo}, falha: {ex}")
                raise HTTPException(detail=f"Falha ao buscar produto com o código: {produto.codigo} falha: {ex}",
                                    status_code=500)
    
    async def CapturarImagens(self, produto:ProductInDB) -> Result[ProductInDB, HTTPException]:
        logger.info(f"Iniciando processo de busca de imagens para produto {produto.nome_produto}")

        semImagens = 0

        if produto.imageUrls is None or produto.imageUrls.__len__() == semImagens:
            logger.info(f"O produto não possui imagens: {produto.nome_produto}")

            quantidadeResultados = 5
            buscarPorImagens = True

            listaDeResultadosDeBusca = GooglePseService.search_google_pse(api_key=settings.GOOGLE_PSE_KEY,
                                                                          search_engine_id=settings.GOOGLE_PSE_ID,
                                                                          query=produto.nome_produto,
                                                                          image=buscarPorImagens,
                                                                          count=quantidadeResultados)
            
            produto.imageUrls = GooglePseUtils.ExtrairLinksDeImagens(listaDeResultadosDeBusca)
        
        else:
            logger.info(f"Produto já possui imagens em banco")

        return produto
            
    async def AtualizarProduto(self, produto:ProductInDB) -> Result[ProductInDB, HTTPException]:
        try:
            logger.info(f"Iniciando processo de atualização de produto com o código:{produto.codigo}")

            result = await self.mongoDb.update_one({'_id': ObjectId(produto.id)}, {'$set':{'atualizado': produto.atualizado,
                                                                                           'DescricaoTecnica': produto.descricao_tecnica,
                                                                                           'ImageUrls': produto.imageUrls}})

            logger.debug(f"Produto atualizado com o id {produto.id} atualizado no banco: {result}")

            return produto
        
        except Exception as ex:
            logger.error(f"Falha ao atualizar o produto com o código: {produto.codigo}, falha: {ex}")
            raise HTTPException(detail=f"Falha ao atualizar o produto com o código: {produto.codigo} falha: {ex}",
                                status_code=500)

    async def BuscarProdutosEmBanco(self, pagina:int, itensPorPagina:int) -> Optional[list[ProductToShow]]:
        try:
            logger.info("Iniciando processo de recuperar produtos por página")

            offset = (pagina - 1) * itensPorPagina

            retornar = 1
            naoRetornar = 0

            produtos:list[ProductToShow] = await self.mongoDb.find({}, projection={"_id": naoRetornar,
                                                               "Codigo": retornar, 
                                                               "NomeProduto":retornar, 
                                                               "Status": retornar,
                                                               "Categoria": retornar,
                                                               "urlImagem": {"$ifNull": [{ "$arrayElemAt": ["$ImageUrls", 0] }, "Sem imagem"] }}).skip(offset).limit(itensPorPagina).to_list(length=None)

            semProdutos = 0

            if produtos is None or produtos.count == semProdutos:
                logger.error(f"Não encontrado produtos da página {pagina}")
                raise HTTPException(detail = f"Não encontrado produtos da página {pagina}",
                                    status_code = 404)
            
            logger.info(f"Produtos retornados do banco de dados: {produtos}")

            produtos = await self.RemoverProdutosVazios(produtos)

            return produtos

        except Exception as ex:
            logger.error(f"Ocorreu uma falha ao tentar buscar os produtos por página: {ex}")

    async def RemoverProdutosVazios(self, produtos:list[ProductToShow]) -> list[ProductToShow]:
        
        produtoContador = 1

        produtosCorretos:list[ProductToShow] = []

        logger.debug(f"Quantidade de produtos: {produtos.__len__()}")

        for produto in produtos:
            try:
                logger.debug(f"Produto -> {produto} - identificador: {produtoContador}")

                if  produto.get("Codigo", None):
                    logger.debug(f"Produto correto: {produto} - identificador: {produtoContador}")
                    produtosCorretos.append(produto)
                    produtoContador+=1
                    continue
                else:
                    logger.warning(f"Removido produto: {produto} - identificador: {produtoContador}")
                    produtoContador+=1

            except Exception as ex:
                    logger.error(f"Removido produto: {produto} - identificador: {produtoContador} - {ex}")
                    produtos.remove(produto)
                    produtoContador+=1
                    continue
            
        logger.debug(f"Quantidade ao final: {produtosCorretos.__len__()}")

        return produtosCorretos

    #endregion

    #region método para pipeline
        
    async def Pipeline(self, code):
        produto = await self.BuscarRegistroEmBanco(code)

        if settings.USE_GEMINI:
            produto = await self.GerarDescricaoTecnicaComGemini(produto)

        produto = await self.GerarDescricaoTecnica(produto)
        produto = await self.CapturarImagens(produto)
        produto = await self.AtualizarProduto(produto)
        return produto
            
    #endregion

    async def get_product_by_code(self, code:str) -> Optional[ProductInDB]:
        product = await self.Pipeline(code)
        return product
    
    async def get_top_products(self, page:int, itensByPage:int) -> Optional[list[ProductToShow]]:

        products = await self.BuscarProdutosEmBanco(page, itensByPage)

        return products