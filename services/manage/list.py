import os
from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse
from app.internal.response_model import ResponseModel

router = APIRouter()

async def list(request: Request):
    try:
        html_content = f"""
        <!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Repo Analyzer</title>
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
            text-align: center;
        }}
        h1 {{
            color: #333;
        }}
        p {{
            line-height: 1.6;
            color: #555;
        }}
        .button {{
            display: inline-block;
            margin: 10px;
            padding: 10px 20px;
            font-size: 16px;
            color: #fff;
            background-color: #007bff;
            border: none;
            border-radius: 5px;
            text-decoration: none;
            transition: background-color 0.3s;
        }}
        .button:hover {{
            background-color: #0056b3;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Repo Analyzer</h1>
        <p>Please choose an option below:</p>
        <a href="/deepseek/chat" class="button">Analyze Repo</a>
        <a href="/deepseek/error" class="button">Evaluate errors</a>
        <a href="/deepseek/roadmap" class="button">Generate a Roadmap</a>
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
