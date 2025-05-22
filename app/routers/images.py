from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
import os
from app.models.product import ImageRequest
from app.services.image_service import ImageService
from app.models.user import UserInDB
from app.services.auth_service import AuthService
from app.core.config import settings
from app.core.security import decode_token

router = APIRouter(tags=["Images"])

#region Authenticação
async def get_current_user(token: str = Depends(decode_token)):
    user = AuthService.get_user(token.get("sub"))
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return user
#endregion

#region Rotas para imagens

@router.post("/upload-product-image/{product_code}")
async def upload_product_image(
    product_code: str,
    file: UploadFile = File(...),
    current_user: UserInDB = Depends(get_current_user)):

    request = ImageRequest(
        code=product_code,
        file=file)
    
    imageService = ImageService(requisicao=request)

    return await imageService.UploadImage()

@router.get("/images/{product_code}")
async def get_product_image(product_code: str):

    request = ImageRequest(code=product_code)

    imageService = ImageService(requisicao=request)

    return await imageService.ShowImage()

#endregion