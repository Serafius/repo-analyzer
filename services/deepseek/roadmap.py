import os
from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse
from utils.html import error_html, html_content

router = APIRouter()


async def roadmap(request: Request):
    try:
        save_dir = os.path.abspath(os.path.join(os.getcwd(), "repo"))
        file_path = os.path.join(save_dir, "compressed_output.txt")

        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()

        feedback_prompt = "Analyze the given code repository to generate a structured product roadmap. The roadmap should be divided into short-term (0-3 months), mid-term (3-6 months), and long-term (6+ months) goals."

        prompt = f"{file_content}\n\n{feedback_prompt}"

        model = request.app.state.model
        tokenizer = request.app.state.tokenizer

        input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)
        input_length = input_ids.shape[1]  # Number of tokens in the prompt

        model.generation_config.pad_token_id = tokenizer.pad_token_id

        output = model.generate(
            input_ids=input_ids,
            max_new_tokens=1000,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
            do_sample=True,
        )

        new_tokens = output[0][input_length:]
        generated_text = tokenizer.decode(new_tokens, skip_special_tokens=True)

        return HTMLResponse(content=html_content(generated_text), status_code=status.HTTP_200_OK)

    except Exception as error:
        return HTMLResponse(
            content=error_html(error), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
