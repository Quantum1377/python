import os
import requests

# Lê o token de acesso da Hugging Face do ambiente
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
MODEL = "stabilityai/stable-diffusion-2"

def generate_image(prompt: str):
    """Envia prompt à API da Hugging Face e retorna bytes da imagem gerada."""
    if not HF_TOKEN:
        raise ValueError("Token Hugging Face ausente. Exporte HUGGINGFACE_TOKEN no ambiente.")
    
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL}",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        raise Exception(f"Erro na geração: {response.text}")
    
    return response.content
