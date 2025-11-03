from database import init_db, save_user, get_all_users
from utils import capture_image_from_webcam, get_face_encoding_from_image
import sys

def register():
    init_db()
    username = input("Nome de usuário para registrar: ").strip()
    if username == "":
        print("Nome vazio. Abortando.")
        return
    # checar se já existe
    users = get_all_users()
    if any(u["username"].lower() == username.lower() for u in users):
        print("Usuário já cadastrado.")
        return

    print("Abra a webcam. Posicione-se e pressione SPACE para tirar a foto.")
    img = capture_image_from_webcam()
    if img is None:
        print("Captura cancelada.")
        return

    encoding, err = get_face_encoding_from_image(img)
    if err:
        print("Erro:", err)
        return

    save_user(username, encoding)
    print(f"Usuário '{username}' registrado com sucesso!")

if __name__ == "__main__":
    try:
        register()
    except Exception as e:
        print("Erro:", e)
        sys.exit(1)
