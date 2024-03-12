import cv2

def dibujar_zonas_con_centro(frame):
    alto, ancho = frame.shape[:2]
    
    # Calcular el centro y las separaciones
    centro_x, centro_y = ancho // 2, alto // 2
    cuarto_x, cuarto_y = ancho // 4, alto // 4

    # Dibujar rectángulo en el centro
    esquina_sup_izq = (cuarto_x, cuarto_y)
    esquina_inf_der = (cuarto_x * 3, cuarto_y * 3)
    cv2.rectangle(frame, esquina_sup_izq, esquina_inf_der, (0, 255, 0), 2)
    
    # Dibujar líneas desde las esquinas del rectángulo hasta las esquinas de la imagen
    cv2.line(frame, esquina_sup_izq, (0, 0), (0, 255, 0), 2)
    cv2.line(frame, (esquina_sup_izq[0], esquina_inf_der[1]), (0, alto), (0, 255, 0), 2)
    cv2.line(frame, (esquina_inf_der[0], esquina_sup_izq[1]), (ancho, 0), (0, 255, 0), 2)
    cv2.line(frame, esquina_inf_der, (ancho, alto), (0, 255, 0), 2)
    
    return frame

# Inicializar la captura de video
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Procesar el fotograma para dibujar las zonas y el centro
    frame_con_zonas = dibujar_zonas_con_centro(frame)
    
    # Mostrar el resultado
    cv2.imshow("Webcam con Zonas y Centro", frame_con_zonas)
    
    # Romper el bucle con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
