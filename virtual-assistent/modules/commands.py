import webbrowser
from datetime import datetime
import re
import os
from modules.voice import say

def handle_command(text: str) -> bool:
    """
    Retorna True se o comando foi reconhecido e tratado.
    Comandos implementados (texto livre em pt-BR/EN simples):
    - hora / que horas sao
    - abrir youtube / abrir google / abrir <site>
    - pesquisar <termo>
    - tocar musica / tocar arquivo <caminho>
    - ajuda
    - sair / encerrar
    """
    t = text.strip().lower()

    # SAIR
    if re.search(r'\b(sair|encerrar|fechar|tchau)\b', t):
        say("Encerrando. Até mais!")
        print("Encerrando assistente...")
        raise SystemExit(0)

    # AJUDA
    if re.search(r'\b(ajuda|comandos|o que voce pode|help)\b', t):
        help_text = (
            "Eu posso:\n"
            "- dizer as horas (ex: 'que horas são')\n"
            "- abrir sites (ex: 'abrir youtube')\n"
            "- pesquisar no Google (ex: 'pesquisar python')\n"
            "- tocar música (ex: 'tocar musica' ou 'tocar arquivo caminho')\n"
            "- responder perguntas simples (se conectado ao AI)\n"
            "- encerrar (diga 'sair')"
        )
        say(help_text)
        print(help_text)
        return True

    # HORAS
    if re.search(r'\b(hora|que horas|horas)\b', t):
        now = datetime.now()
        text_out = f"Agora são {now.hour:02d}h{now.minute:02d}."
        say(text_out)
        print(text_out)
        return True

    # ABRIR SITES COMUNS
    if re.search(r'\b(abrir|abre)\b', t):
        # tenta detectar site
        if 'youtube' in t:
            say("Abrindo YouTube")
            webbrowser.open("https://www.youtube.com")
            return True
        if 'google' in t:
            say("Abrindo Google")
            webbrowser.open("https://www.google.com")
            return True
        # pega algo após "abrir"
        m = re.search(r'abrir (.+)', t)
        if m:
            target = m.group(1).strip()
            url = target if target.startswith("http") else f"https://{target.replace(' ','')}"
            say(f"Abrindo {target}")
            webbrowser.open(url)
            return True

    # PESQUISAR (abre Google com query)
    m = re.search(r'\b(pesquisar|procure por|buscar)\b (.+)', t)
    if m:
        query = m.group(2)
        say(f"Pesquisando por {query}")
        url = "https://www.google.com/search?q=" + query.replace(" ", "+")
        webbrowser.open(url)
        return True

    # TOCAR MÚSICA — procura arquivo local
    if re.search(r'\b(tocar musica|tocar música)\b', t):
        # tenta abrir pasta default "music" ou pedir caminho
        music_folder = os.path.expanduser("~/Music")
        if os.path.isdir(music_folder):
            say("Abrindo pasta de músicas")
            webbrowser.open(f"file://{music_folder}")
        else:
            say("Por favor, informe o caminho do arquivo para tocar.")
        return True

    m = re.search(r'\btocar arquivo (.+)', t)
    if m:
        path = m.group(1).strip().strip('"')
        if os.path.exists(path):
            say("Tocando arquivo.")
            webbrowser.open(f"file://{os.path.abspath(path)}")
        else:
            say("Arquivo não encontrado.")
        return True

    # Abrir aplicativos locais (exemplo simples, apenas para Windows/macOS/Linux)
    m = re.search(r'\b(abra|abrir aplicativo) (.+)', t)
    if m:
        app = m.group(2).strip()
        try:
            say(f"Abrindo {app}")
            if os.name == 'nt':
                os.startfile(app)
            else:
                # tenta chamar pelo shell
                os.system(f"{app} &")
            return True
        except Exception:
            say("Não consegui abrir o aplicativo.")
            return True

    # Se nenhum comando reconhecido:
    return False
