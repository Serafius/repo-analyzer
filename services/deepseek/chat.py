# chat_endpoint.py
from fastapi import APIRouter, Request, status
from app.internal.response_model import ResponseModel

router = APIRouter()

@router.post("/chat", status_code=status.HTTP_200_OK)
async def chat(request: Request, prompt: str):
    """
    Generate a response based on a given prompt.
    """
    try:
        # Access model and tokenizer from app state
        model = request.app.state.model
        tokenizer = request.app.state.tokenizer

        # Tokenize the prompt
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)

        # Generate text
        output = model.generate(
            input_ids=input_ids,
            max_length=50,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
            do_sample=True,
        )

        # Decode the generated text
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

        return ResponseModel(
            data={"response": generated_text},
            isSuccess=True,
            error=None,
            status=status.HTTP_200_OK,
        )

    except Exception as error:
        return ResponseModel(
            data=None,
            isSuccess=False,
            error=str(error),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
