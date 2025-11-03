import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def ask_ai_if_needed(prompt: str) -> str | None:
    """
    Se houver OPENAI_API_KEY no .env, faz uma chamada simples à API OpenAI (Chat completions)
    Retorna string de resposta ou None se não configurado / erro.
    """
    if not OPENAI_API_KEY:
        return None

    try:
        import openai
        openai.api_key = OPENAI_API_KEY
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini", # ou "gpt-4o" dependendo do seu acesso
            messages=[{"role":"user","content":prompt}],
            max_tokens=1000000,
            temperature=0.6
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print("Erro AI:", e)
        return None
