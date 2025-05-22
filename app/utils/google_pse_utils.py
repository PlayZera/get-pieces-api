from app.core.logger import logger
from app.models.google import SearchResult

class GooglePseUtils:
    def ExtrairLinksDeImagens(retornoPesquisa:list[SearchResult]):

        logger.info(f"Iniciando processo de extração de links de imagens no retorno da busca do google")

        listaLinksImagens = []

        for retorno in retornoPesquisa:
            logger.info(f"Tratando retorno individual: {retorno}")

            if retorno.link.lower().endswith(".jpg"):
                listaLinksImagens.append(retorno.link)

        return listaLinksImagens