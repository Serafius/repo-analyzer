# lifespan.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer
from utils.fetch_repo import fetch_github_repo_details, fetch_github_repo_tree
from utils.compress_repo import compress_repo
import torch
import os


load_dotenv()

PORT = int(os.getenv("PORT", 3001))
HF_TOKEN = str(os.getenv("HF_TOKEN"))

model_path = os.path.abspath(os.path.join(os.getcwd(), "model"))
offload_dir = os.path.abspath(os.path.join(model_path, "offload_weights"))


model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
device_map = "auto"
repo_link = "https://github.com/Serafius/data-wallet-express"

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # Load resources on startup
    print(f"Server is starting on port {PORT}")
    print("Model path:", model_path)
    # Load model and tokenizer
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading model on {device}...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map=device_map,
        token=HF_TOKEN,
    )
    tokenizer = AutoTokenizer.from_pretrained(
        model_name, trust_remote_code=True, token=HF_TOKEN
    )
    print("Fetching repo details...")
    repo = await fetch_github_repo_details(repo_link.split("/")[-2], repo_link.split("/")[-1])
    repo_tree = await fetch_github_repo_tree(repo.repo_owner, repo.repo_name, repo.sha)
    compress_repo(repo_link)
    # Attach model and tokenizer to app state
    app.state.repo = repo
    app.state.repo_tree = repo_tree
    app.state.model = model
    app.state.tokenizer = tokenizer
    print("Model and tokenizer loaded successfully!")

    yield  # Wait for app shutdown

    # Cleanup resources on shutdown
    print("Shutting down")
