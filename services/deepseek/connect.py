from fastapi import status
from app.internal.response_model import ResponseModel
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

model_name = "deepseek-ai/deepseek-llm-7b-base"
use_4bit = True
bnb_4bit_compute_dtype = "float16"
bnb_4bit_quant_type = "nf4"
use_nested_quant = False
device_map = "auto"


async def connect():
    try:
        # Config
        compute_dtype = getattr(torch, bnb_4bit_compute_dtype)
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=use_4bit,
            bnb_4bit_quant_type=bnb_4bit_quant_type,
            bnb_4bit_compute_dtype=compute_dtype,
            bnb_4bit_use_double_quant=use_nested_quant,
        )

        # Load model
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,
            device_map=device_map,
            use_auth_token=HF_TOKEN,
        )
        model.config.use_cache = False
        model.config.pretraining_tp = 1.0

        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            model_name, trust_remote_code=True, use_auth_token=HF_TOKEN
        )

        return ResponseModel(
            data={"connect": True},
            isSuccess=True,
            error=None,
            status=status.HTTP_200_OK,
        )

    except Exception as error:
        return ResponseModel(
            data={"url": None},
            isSuccess=False,
            error=error,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
