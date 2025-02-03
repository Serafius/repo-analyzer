def error_html(error):
    return f"""
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


def html_content(message):
    return f"""
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
                <p>{message}</p>
            </div>
        </body>
        </html>
        """


def error_handler_response(evaluations):
    content = """
    <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
                    </head>
            <title>Error Evaluations</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h2 { color: #555; }
                hr { margin: 20px 0; }
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
            <h1>Error Evaluations</h1>
        """
    for evaluation in evaluations:
        content += f"<h2>Error:</h2><p>{evaluation['error']}</p>"
        content += f"<h3>Evaluation:</h3><p>{evaluation['evaluation']}</p><hr/>"
    content += "</div></body></html>"

    return content
