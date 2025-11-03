from modules.voice import listen_voice, say, text_input
from modules.commands import handle_command
from modules.ai_integration import ask_ai_if_needed
import time

def main():
    say("Olá! Assistente iniciado. Diga 'ajuda' para ver comandos.")
    print("Assistente iniciado. Pressione Ctrl+C para sair.\n")

    while True:
        # tenta ouvir por voz, caso não consiga retorna None
        print("Aguardando comando por voz (ou digite no teclado)...")
        user_text = listen_voice(timeout=6, phrase_time_limit=8)
        if user_text is None:
            # fallback para input de texto
            user_text = text_input("Digite o comando (ou pressione Enter para tentar voz novamente): ")
            if not user_text.strip():
                continue

        print(f">>> Você: {user_text}")

        # Checa por comando conhecido e responde; se não souber, pergunta ao AI (opcional)
        handled = handle_command(user_text)
        if not handled:
            # Se quiser usar IA, habilite a linha abaixo (ai key via .env)
            ai_ans = ask_ai_if_needed(user_text)
            if ai_ans:
                say(ai_ans)
                print("Assistente (AI):", ai_ans)
            else:
                say("Desculpe, não entendi esse comando.")
                print("Assistente: comando não reconhecido.")

        # pequena pausa para estabilidade
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        say("Encerrando assistente. Até mais!")
        print("\nEncerrado.")
