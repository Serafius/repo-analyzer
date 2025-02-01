# lifespan.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

load_dotenv()

PORT = int(os.getenv("PORT", 3001))

model_path = os.path.abspath(os.path.join(os.getcwd(), "model"))
offload_dir = os.path.abspath(os.path.join(model_path, "offload_weights"))

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # Load resources on startup
    print(f"Server is starting on port {PORT}")
    print("Model path:", model_path)
    # Load model and tokenizer
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading model on {device}...")
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map="auto",
        offload_folder=offload_dir,
        torch_dtype=torch.float16,
    )
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    # Attach model and tokenizer to app state
    app.state.model = model
    app.state.tokenizer = tokenizer
    print("Model and tokenizer loaded successfully!")

    yield  # Wait for app shutdown

    # Cleanup resources on shutdown
    print("Shutting down")
