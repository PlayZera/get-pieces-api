from fastapi import APIRouter, Depends, HTTPException
from app.models.product import ProductListRequest, ProductResponse
from app.models.user import UserInDB
from app.services.auth_service import AuthService
from app.services.product_service import ProductService
from app.core.security import decode_token
from app.core.logger import logger

router = APIRouter(tags=["Products"])

#region Auth
async def get_current_user(token: str = Depends(decode_token)):
    user = AuthService.get_user(token.get("sub"))
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return user
#endregion

@router.post("/products/import", response_model=ProductResponse)
async def import_products(
    product_request: ProductListRequest,
    current_user: UserInDB = Depends(get_current_user)):
    try:
        service = ProductService()
        products_to_process = product_request.products
        result = service.process_product_list(products_to_process)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao importar produtos: {str(e)}"
        )

@router.get("/products/{product_code}",  response_model=ProductResponse)
async def get_product(
    product_code: str,
    current_user: UserInDB = Depends(get_current_user)
):
    try:
        logger.info("Iniciando processo de busca por código")

        service = ProductService()
        return await service.get_product_info(product_code)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao buscar produto: {str(e)}"
        )

@router.get("/products/", response_model=ProductResponse)
async def get_all_products(
    page: int, 
    itensByPage: int,
    current_user: UserInDB = Depends(get_current_user)
):
    try:
        logger.info("Iniciando processo de busca de produtos por página")

        service = ProductService()

        products = await service.get_top_products(page, itensByPage)

        return products
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar produtos: {str(e)}"
        )