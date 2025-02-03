import os
from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse
from app.internal.response_model import ResponseModel
from utils.html import (
    error_html,
    error_handler_response,
)  # Use your error HTML template

from utils.fetch_repo import (
    fetch_github_repo_details,
    fetch_github_repo_file,
    fetch_github_repo_tree,
)

router = APIRouter()

async def error_handler(request: Request):
    try:
        repo = request.app.state.repo
        logs_file_data = await fetch_github_repo_file(
            repo.repo_owner, repo.repo_name, repo.sha, "error_log.txt"
        )
        if logs_file_data is None:
            return HTMLResponse(
                content=error_html, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        print(logs_file_data)
        # Assume logs_file_data is a string with multiple error lines
        error_entries = [
            line.strip() for line in logs_file_data.splitlines() if line.strip()
        ]

        # The fixed feedback prompt to be appended to each error
        feedback_prompt = (
            "Analyze the error and why it happened. Provide a detailed explanation of the root cause "
            "and potential solutions to prevent similar errors in the future."
        )

        # Access model and tokenizer from the app state
        model = request.app.state.model
        tokenizer = request.app.state.tokenizer

        evaluations = []

        # Loop over each error entry and send it to the model for evaluation
        for error_entry in error_entries:
            prompt = f"{error_entry}\n\n{feedback_prompt}"
            input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(
                model.device
            )
            input_length = input_ids.shape[1]  # Number of tokens in the prompt

            # Ensure the model uses the tokenizer's pad token id for generation
            model.generation_config.pad_token_id = tokenizer.pad_token_id

            # Generate text with the model (adjust max_new_tokens as needed)
            output = model.generate(
                input_ids=input_ids,
                max_new_tokens=250,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                do_sample=True,
            )

            # Decode only the new tokens (i.e. the model’s response)
            new_tokens = output[0][input_length:]
            generated_text = tokenizer.decode(new_tokens, skip_special_tokens=True)

            evaluations.append({"error": error_entry, "evaluation": generated_text})

        return HTMLResponse(
            content=error_handler_response(evaluations), status_code=status.HTTP_200_OK
        )

    except Exception as error:
        # Optionally log the error details here before returning the error response.
        return HTMLResponse(
            content=error_html(error), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
