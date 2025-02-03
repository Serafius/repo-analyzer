from fastapi import status, Depends, APIRouter
from app.internal.response_model import ResponseModel
from services import list as listOptions

router = APIRouter()

@router.get("/")
async def list(response: ResponseModel = Depends(listOptions)):
    return response