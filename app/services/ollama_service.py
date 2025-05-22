import requests
from fastapi import HTTPException

from app.models.google import SearchResult
from ..core.config import settings
from app.core.logger import logger
import time

class OllamaService:
    @staticmethod
    def get_technical_description(product_info: dict, web_product_info: list[SearchResult]) -> str:
        prompt = f"""
        Com base nestas informações do produto:

        { {k: v for k, v in product_info.items() if k != 'image_url'} }

        Com base nestas informações da web:

        { {retornoPesquisa.link for retornoPesquisa in web_product_info} }
        
        Você é um assistente, que deve fornecer informações de peças que lhe é informado, todas as respostas devem estar em português.

        Você deve exibir uma descrição técnica resumida baseada nas informações que lhe é fornecido somente sobre o produto.

        Informações como telefone e email não devem ser exibidas na resposta.

        Você deve formatar as respostas em markdown.

        ## Descrição técnica
        ## Site oficial
        ## Exemplos de uso
        """
        payload = {
            "model": settings.MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            logger.info(f"Chamando API Ollama - Modelo de linguagem - {settings.MODEL_NAME}.")

            inicioTimer = time.time()
            logger.info(f"Iniciando timer para gerar descrição - {inicioTimer}")

            response = requests.post(settings.OLLAMA_API_URL, json=payload)
            response.raise_for_status()

            tempoPassado = time.time()
            tempoPassado = tempoPassado - inicioTimer
            logger.info(f"Finalizado timer para gerar descrição - {tempoPassado:.4f} segundos")

            descricaoTecnica = response.json().get("response", "")

            logger.debug(f"Resposta retornada pela API - Prompt: {prompt} Descrição técnica: {descricaoTecnica}")

            logger.info("Descrição técnica gerada com sucesso.")
            return descricaoTecnica
        
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao conectar com a API Ollama: {str(e)}"
            )
        