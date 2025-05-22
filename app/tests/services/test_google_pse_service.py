from app.models.google import SearchResult
from app.services.google_pse_service import GooglePseService

def Teste_BuscaPorItemGoogle(secretKey:str, searchId:str, query:str, index:int):
    print(f"Iniciando processo de pesquisa no google secretKey:{secretKey}, searchId:{searchId}, query:{query}, index:{index}")
    result = GooglePseService.search_google_pse(secretKey, searchId, query, index)

    result = list[SearchResult](result)
    
    print(f"Resultado busca no google: {result}")

    listaLinks = ExtrairLinksDeImagens(retornoPesquisa=result)

    print(f"Links de imagens retorandos: {listaLinks}")


def ExtrairLinksDeImagens(retornoPesquisa:list[SearchResult]):

    print(f"Iniciando processo de extração de links de imagens no retorno da busca do google")

    listaLinksImagens = [str]

    for retorno in retornoPesquisa:
        print(f"Tratando retorno individual: {retorno}")

        if retorno.link.lower().endswith(".jpg"):
            listaLinksImagens.append(retorno.link)
    
    return listaLinksImagens
            

        
