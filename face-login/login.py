from database import init_db, get_all_users, log_login
from utils import capture_image_from_webcam, get_face_encoding_from_image, compare_encodings
from datetime import datetime
import numpy as np
import sys

def login():
    init_db()
    users = get_all_users()
    if len(users) == 0:
        print("Nenhum usuário cadastrado. Registre um usuário primeiro.")
        return

    print("Abra a webcam para autenticar. Pressione SPACE para capturar foto.")
    img = capture_image_from_webcam()
    if img is None:
        print("Captura cancelada.")
        return

    unknown_encoding, err = get_face_encoding_from_image(img)
    if err:
        print("Erro:", err)
        return

    known_encodings = [u["encoding"] for u in users]
    idx, dist = compare_encodings(known_encodings, unknown_encoding, tolerance=0.5)  # ajustar tol
    if idx is None:
        print(f"Nenhuma correspondência (melhor distância: {dist:.3f}). Acesso negado.")
    else:
        matched_user = users[idx]
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_login(matched_user["id"], matched_user["username"], ts)
        print(f"✅ Usuário autenticado: {matched_user['username']}  (distância {dist:.3f})")
        print(f"Login registrado em {ts}")

if __name__ == "__main__":
    try:
        login()
    except Exception as e:
        print("Erro:", e)
        sys.exit(1)
