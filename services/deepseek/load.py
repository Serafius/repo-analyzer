from dotenv import load_dotenv
import os
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)

load_dotenv()
HF_TOKEN = str(os.getenv("HF_TOKEN"))

model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
use_4bit = True
bnb_4bit_compute_dtype = "float16"
bnb_4bit_quant_type = "nf4"
use_nested_quant = False
device_map = "auto"
save_dir = os.path.abspath(os.path.join(os.getcwd(), "model"))
offload_dir = os.path.abspath(os.path.join(save_dir, "offload_weights"))


def load():
    try:
        os.makedirs(save_dir, exist_ok=True)
        os.makedirs(offload_dir, exist_ok=True)
        print("CUDA Available:", torch.cuda.is_available())
        print(
            "CUDA Device Name:",
            (
                torch.cuda.get_device_name(0)
                if torch.cuda.is_available()
                else "No GPU found"
            ),
        )

        print("Loading model")
        # Load model
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map=device_map,
            token=HF_TOKEN,
        )
        model.config.use_cache = False
        model.config.pretraining_tp = 1.0

        print("Loading tokenizer")
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            model_name, trust_remote_code=True, token=HF_TOKEN
        )

        print("Saving model and tokenizer")
        # Save model and tokenizer
        model.save_pretrained(save_dir, safe_serialization=False)
        tokenizer.save_pretrained(save_dir, safe_serialization=False)

    except Exception as error:
        print(error)
        print("Error loading model")
        return error

load()