from fastapi import status, Depends, APIRouter
from app.internal.response_model import ResponseModel

router = APIRouter()

@router.post("/connect")
async def connect():
    try:    
        return ResponseModel(data={"connection": True}, isSuccess=True, error=None, status=status.HTTP_200_OK)
    except Exception as error:
        return ResponseModel(data=None, isSuccess=False, error=error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    