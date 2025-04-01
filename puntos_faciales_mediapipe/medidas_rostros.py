import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=2, 
                                  min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Captura de video
cap = cv2.VideoCapture(0)

# Lista de índices de landmarks específicos (ojos y boca)
selected_points = [
    33, 133, # ojo izquierdo
    362, 263, # ojo derecho
    61, 291, # boca
    8, 19, # nariz 
    5, 468, # punta de la nariz al iris izq 
    5, 473 # punta de la nariz al iris derecho
]

def distancia(p1, p2):
    """Calcula la distancia euclidiana entre dos puntos."""
    return np.linalg.norm(np.array(p1) - np.array(p2))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Espejo para mayor naturalidad
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            puntos = {}
            
            for idx in selected_points:
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos[idx] = (x, y)
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)  # Dibuja el punto en verde
            
            # Calcular y mostrar distancia entre puntos (ejemplo: entre ojos)
            if 33 in puntos and 133 in puntos:
                d_ojos = distancia(puntos[33], puntos[133])
                
                cv2.line(frame, (puntos[33][0], puntos[33][1]), (puntos[133][0], puntos[133][1]), (23, 234, 23), 2)	

                cv2.putText(frame, f"D: {int(d_ojos)}", (puntos[33][0], puntos[33][1] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            if 362 in puntos and 263 in puntos:
                d_ojos = distancia(puntos[362], puntos[263])
                
                cv2.line(frame, (puntos[362][0], puntos[362][1]), (puntos[263][0], puntos[263][1]), (23, 234, 23), 2)	

                cv2.putText(frame, f"D: {int(d_ojos)}", (puntos[362][0], puntos[362][1] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            if 61 in puntos and 291 in puntos:
                d_ojos = distancia(puntos[61], puntos[291])
                
                cv2.line(frame, (puntos[61][0], puntos[61][1]), (puntos[291][0], puntos[291][1]), (23, 234, 23), 2)	

                cv2.putText(frame, f"D: {int(d_ojos)}", (puntos[61][0], puntos[61][1] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            if 8 in puntos and 19 in puntos:
                d_ojos = distancia(puntos[8], puntos[19])
                
                cv2.line(frame, (puntos[8][0], puntos[8][1]), (puntos[19][0], puntos[19][1]), (23, 234, 23), 2)	

                cv2.putText(frame, f"D: {int(d_ojos)}", (puntos[8][0], puntos[8][1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            if 5 in puntos and 468 in puntos:
                d_ojos = distancia(puntos[5], puntos[468])
                
                cv2.line(frame, (puntos[5][0], puntos[5][1]), (puntos[468][0], puntos[468][1]), (23, 23, 234), 2)	

                cv2.putText(frame, f"D: {int(d_ojos)}", (puntos[5][0], puntos[5][1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            if 5 in puntos and 473 in puntos:
                d_ojos = distancia(puntos[5], puntos[473])
                
                cv2.line(frame, (puntos[5][0], puntos[5][1]), (puntos[473][0], puntos[473][1]), (23, 23, 234), 2)	

                cv2.putText(frame, f"D: {int(d_ojos)}", (puntos[5][0], puntos[5][1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow('PuntosFacialesMediaPipe', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()