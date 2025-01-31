from fastapi import status, Depends, APIRouter
from app.internal.response_model import ResponseModel
from services import connect as connectDeepseek

router = APIRouter()

@router.get("/connect")
async def get_checkout(response: ResponseModel = Depends(connectDeepseek)):
    return response