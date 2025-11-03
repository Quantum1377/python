import cv2
import face_recognition
import numpy as np
from datetime import datetime

def capture_image_from_webcam(window_name="Capture - press SPACE to take photo, ESC to exit"):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Não foi possível abrir a webcam (index 0).")

    img = None
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        display = frame.copy()
        cv2.putText(display, "Pressione SPACE para capturar, ESC para sair", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        cv2.imshow(window_name, display)
        key = cv2.waitKey(1)
        if key % 256 == 27:  # ESC
            img = None
            break
        elif key % 256 == 32:  # SPACE
            img = frame
            break

    cap.release()
    cv2.destroyAllWindows()
    return img

def get_face_encoding_from_image(image):
    # image: BGR (OpenCV). face_recognition expects RGB.
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb)
    if len(boxes) == 0:
        return None, "Nenhum rosto detectado."
    # pegar primeiro rosto
    encodings = face_recognition.face_encodings(rgb, boxes)
    if len(encodings) == 0:
        return None, "Não foi possível extrair encoding do rosto."
    return encodings[0], None

def compare_encodings(known_encodings, unknown_encoding, tolerance=0.5):
    # known_encodings: lista de np arrays
    if len(known_encodings) == 0:
        return None, None
    distances = face_recognition.face_distance(known_encodings, unknown_encoding)
    best_idx = np.argmin(distances)
    best_dist = distances[best_idx]
    if best_dist <= tolerance:
        return best_idx, best_dist
    return None, best_dist
