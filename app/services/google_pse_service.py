from typing import Optional

import requests
from app.models.google import SearchResult
from app.utils.google_pse_utils import GooglePseUtils
from app.core.logger import logger

class GooglePseService:
    def search_google_pse(
    api_key: str,
    search_engine_id: str,
    query: str,
    count: int,
    image: bool = False,
    filter_list: Optional[list[str]] = None,
) -> list[SearchResult]:
        
        inicioBusca = 1

        url = "https://www.googleapis.com/customsearch/v1"
        headers = {"Content-Type": "application/json"}
        all_results = []
        start_index = inicioBusca
    
        while count > 0:
            num_results_this_page = min(count, 10)

            params = {
                "cx": search_engine_id,
                "q": query,
                "key": api_key,
                "num": num_results_this_page,
                "searchType": "image" if image else "searchTypeUndefined",
                "start": start_index,
            }

            response = requests.request("GET", url, headers=headers, params=params)
            response.raise_for_status()
            json_response = response.json()
            results = json_response.get("items", [])

            if results: 
                all_results.extend(results)
                count -= len(
                    results
                )  
                start_index += 10  
            else:
                break
            
        if filter_list:
            all_results = GooglePseUtils.get_filtered_results(all_results, filter_list)

        logger.info(f"Concluída busca no google: {all_results}")

        return [
            SearchResult(
                link=result["link"],
                title=result.get("title"),
                snippet=result.get("snippet"),
            )
            for result in all_results
        ]

    