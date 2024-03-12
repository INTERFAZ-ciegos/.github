import cv2
import pyautogui
import keyboard  # Agrega esta línea

# Carga los clasificadores en cascada para los ojos y la cara
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


#no jala esa madre

# Inicializa la captura de video
cap = cv2.VideoCapture(0)
import cv2

# Inicializa la posición del ojo
eye_position = None

# Inicializa el estado del ojo
eye_open = True



while(True):
    # Si se presiona la tecla "espacio", se rompe el bucle
    if keyboard.is_pressed('space'):  # Agrega esta línea
        break  # Agrega esta línea

    # Captura cuadro por cuadro
    ret, frame = cap.read()

    # Convierte el cuadro a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecta las caras
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        # Dibuja un rectángulo alrededor de la cara
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        
        # Recorta la cara en la imagen en escala de grises y en la imagen a color
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        # Detecta los ojos dentro de la cara
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) > 0:
            # Si no se ha detectado ningún ojo antes, guarda la posición del primer ojo detectado
            if eye_position is None:
                eye_position = eyes[0]
            (ex,ey,ew,eh) = eye_position
            
            
            
            # Calcula el centro del ojo
            center_x = ex + ew // 2
            center_y = ey + eh // 2
            # Elige el radio más pequeño entre la mitad del ancho y la mitad de la altura del ojo para ajustarse al tamaño de la pupila
            radius = min(ew, eh) // 4
            
            # Dibuja un círculo rosado pequeño del tamaño de la pupila
            cv2.circle(roi_color, (center_x, center_y), radius, (147, 20, 255), 2)  # Color rosa en formato BGR
        

            # Mueve el cursor del mouse basado en la posición del primer ojo detectado
            # Asegúrate de convertir las coordenadas del ojo a coordenadas absolutas de la pantalla
            pyautogui.moveTo(x + ex, y + ey)
            
            # Si el ojo estaba abierto y ahora está cerrado, haz clic
            if eye_open and len(eyes) == 1:
                pyautogui.click()
                eye_open = False
            elif not eye_open and len(eyes) == 2:
                eye_open = True

    # Muestra el cuadro resultante
    cv2.imshow('frame', frame)
    
    # Si presionas 'q' en tu teclado, se cerrará la ventana
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cuando todo esté hecho, libera la captura
cap.release()
cv2.destroyAllWindows()


