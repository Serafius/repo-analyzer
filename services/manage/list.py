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
                <p>Thank you for your feedback. Please choose an option below:</p>
                <ul>
                    <li><a href="/deepseek/chat">Chat</a></li>
                    <li><a href="/deepseek/error">Error Handler</a></li>
                    <li><a href="/deepseek/roadmap">Roadmap</a></li>
                </ul>
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
