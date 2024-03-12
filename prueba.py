import cv2
import pyautogui
import keyboard

eye_open = True


# Carga los clasificadores en cascada para los ojos y la cara
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def dibujar_zonas_con_centro(frame):
    alto, ancho = frame.shape[:2]
    centro_x, centro_y = ancho // 2, alto // 2   
    sexto_x, sexto_y = ancho // 6, alto // 6
 
    esquina_sup_izq = (centro_x - sexto_x, centro_y - sexto_y)
    esquina_inf_der = (centro_x + sexto_x, centro_y + sexto_y)
    cv2.rectangle(frame, esquina_sup_izq, esquina_inf_der, (0, 255, 0), 2)
    
    # Dibujar líneas adicionales para demarcar las zonas visualmente
    cv2.line(frame, esquina_sup_izq, (0, 0), (0, 255, 0), 2)
    cv2.line(frame, (esquina_sup_izq[0], esquina_inf_der[1]), (0, alto), (0, 255, 0), 2)
    cv2.line(frame, (esquina_inf_der[0], esquina_sup_izq[1]), (ancho, 0), (0, 255, 0), 2)
    cv2.line(frame, esquina_inf_der, (ancho, alto), (0, 255, 0), 2)
    
    return frame, esquina_sup_izq, esquina_inf_der

cap = cv2.VideoCapture(0)
eye_position = None

while(True):
    if keyboard.is_pressed('space'):
        break

    ret, frame = cap.read()
    frame, esquina_sup_izq, esquina_inf_der = dibujar_zonas_con_centro(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        if eye_position is None:
            eyes = eye_cascade.detectMultiScale(roi_gray)
            if len(eyes) > 0:
                (ex,ey,ew,eh) = eyes[0]
                eye_position = (ex, ey, ew, eh)

        if eye_position:
            (ex,ey,ew,eh) = eye_position
            center_x = x + ex + ew // 2
            center_y = y + ey + eh // 2
            radius = min(ew, eh) // 4
            cv2.circle(roi_color, (ex + ew // 2, ey + eh // 2), radius, (147, 20, 255), 2)
            
            # Determinar en qué zona está el ojo y mover el mouse en consecuencia
            if center_x < esquina_sup_izq[0]:
                pyautogui.move(-10, 0)  # Mover izquierda
            elif center_x > esquina_inf_der[0]:
                pyautogui.move(10, 0)  # Mover derecha
            if center_y < esquina_sup_izq[1]:
                pyautogui.move(0, -10)  # Mover arriba
            elif center_y > esquina_inf_der[1]:
                pyautogui.move(0, 10)  # Mover abajo
            
            # Si el ojo estaba abierto y ahora está cerrado, haz clic
            if eye_open and len(eyes) == 1:
                pyautogui.click()
                eye_open = False
            elif not eye_open and len(eyes) == 2:
                eye_open = True


    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
