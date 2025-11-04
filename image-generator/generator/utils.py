import base64
import os
from datetime import datetime

def save_image(image_bytes: bytes, output_folder: str) -> str:
    """Salva a imagem gerada localmente e retorna o caminho relativo."""
    os.makedirs(output_folder, exist_ok=True)
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
    path = os.path.join(output_folder, filename)
    with open(path, "wb") as f:
        f.write(image_bytes)
    return path
