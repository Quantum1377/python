import speech_recognition as sr
import pyttsx3
import sys

_engine = None

def _init_tts():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        # Opcional: ajustar voz/velocidade
        rate = _engine.getProperty('rate')
        _engine.setProperty('rate', int(rate * 0.95))
    return _engine

def say(text: str):
    """Fala o texto (TTS) — não bloqueante em CLI simples."""
    try:
        engine = _init_tts()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        # fallback: print
        print("[TTS erro]", e)
        print("Assistente:", text)

def listen_voice(timeout: int = 5, phrase_time_limit: int = 6):
    """
    Escuta voz via microfone e retorna texto. Em caso de erro, retorna None.
    timeout: quanto tempo espera por silêncio inicial
    phrase_time_limit: tempo máximo da frase
    """
    r = sr.Recognizer()
    mic = None
    try:
        mic = sr.Microphone()
    except Exception as e:
        print("Microfone não encontrado ou inacessível:", e)
        return None

    with mic as source:
        try:
            r.adjust_for_ambient_noise(source, duration=0.6)
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = r.recognize_google(audio, language="pt-BR")
            return text
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("Não entendi o áudio.")
            return None
        except sr.RequestError as e:
            print("Erro no serviço de reconhecimento:", e)
            return None
        except Exception as e:
            print("Erro ao ouvir:", e)
            return None

def text_input(prompt: str = "> "):
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
        sys.exit(0)
    except Exception:
        return ""
