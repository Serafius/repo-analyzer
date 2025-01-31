from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import deepseek_router
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()
PORT = int(os.getenv("PORT", 5723))


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(deepseek_router, prefix="/deepseek")


@app.get("/")
async def root():
    return "Server ready"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
