import os
from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse
from app.internal.response_model import ResponseModel

from utils.fetch_repo import fetch_github_repo_details, fetch_github_repo_file, fetch_github_repo_tree
router = APIRouter()

async def error_handler(request: Request):
    try:
        repo = request.app.state.repo
        file = await fetch_github_repo_tree(repo.repo_owner, repo.repo_name, repo.sha)
        return ResponseModel(
                    data={"connect": file},
                    isSuccess=True,
                    error=None,
                    status=status.HTTP_200_OK,
                )        # Define the directory and file path
        save_dir = os.path.abspath(os.path.join(os.getcwd(), "repo"))
        file_path = os.path.join(save_dir, "compressed_output.txt")

        # Read the file content
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()

        # Define the fixed feedback prompt
        feedback_prompt = "Evaluate this system from three perspectives: architecture, security, and software best practices. Assess its scalability, maintainability, and efficiency, identifying potential bottlenecks or improvements. Analyze security risks, including authentication, data protection, and vulnerabilities to common attacks, with recommendations for enhancement. Review code quality, adherence to design patterns, and maintainability, highlighting anti-patterns or areas where best practices like SOLID, DRY, and proper error handling could be better applied. Provide specific examples and alternative approaches where relevant."

        # Combine the file content with the feedback prompt
        prompt = f"{file_content}\n\n{feedback_prompt}"

        # Access model and tokenizer from the app state
        model = request.app.state.model
        tokenizer = request.app.state.tokenizer

        # Tokenize the combined prompt
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)
        input_length = input_ids.shape[1]  # Number of tokens in the prompt

        # Ensure the model uses the tokenizer's pad token id for generation
        model.generation_config.pad_token_id = tokenizer.pad_token_id

        # Generate text using the model with max_new_tokens set to generate 50 additional tokens
        output = model.generate(
            input_ids=input_ids,
            max_new_tokens=500,  # Generate 50 new tokens on top of the input prompt
            temperature=0.7,
            top_k=50,
            top_p=0.95,
            do_sample=True,
        )

        # Decode only the new tokens (i.e., remove the prompt part)
        new_tokens = output[0][input_length:]
        generated_text = tokenizer.decode(new_tokens, skip_special_tokens=True)

        # Create an HTML page with basic styling to display the generated response
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Feedback Response</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background-color: #f9f9f9;
                }}
                .container {{
                    max-width: 800px;
                    margin: auto;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 5px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    text-align: center;
                    color: #333;
                }}
                p {{
                    line-height: 1.6;
                    color: #555;
                    white-space: pre-wrap;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Feedback Response</h1>
                <p>{generated_text}</p>
            </div>
        </body>
        </html>
        """

        return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)

    except Exception as error:
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Error</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background-color: #f9f9f9;
                }}
                .container {{
                    max-width: 800px;
                    margin: auto;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 5px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    text-align: center;
                    color: red;
                }}
                p {{
                    line-height: 1.6;
                    color: #555;
                    white-space: pre-wrap;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Error</h1>
                <p>{str(error)}</p>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(
            content=error_html, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
