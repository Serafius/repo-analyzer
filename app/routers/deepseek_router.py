from fastapi import status, Depends, APIRouter
from app.internal.response_model import ResponseModel
from services import connect as connectDeepseek
from services import chat as chatDeepseek
from services import error_handler as error_handler

router = APIRouter()

@router.get("/connect")
async def connect(response: ResponseModel = Depends(connectDeepseek)):
    return response

@router.get("/chat")
async def chat(response: ResponseModel = Depends(chatDeepseek)):
    return response

@router.get("/error")
async def error(response: ResponseModel = Depends(error_handler)):
    return response