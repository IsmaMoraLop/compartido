# Código para el tratamiento de la imagen

# matrices y funciones matemáticas
import numpy as np
# opencv para imágenes, en concreto, para difuminado de rostros
import cv2

# buffer: imagen analizada en bytes
# response: respuesta de la llamada a Amazon Rekognition
def anonymize_face(buffer, response):
    # Leer la imagen del buffer y cargarla en memoria
    nparr = np.fromstring(buffer, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Recoge la altura y anchura total de la imagen
    height, width, _ = img.shape

    # Bucle para iterar sobre los detalles de los diferentes rostros
    # que el servicio de análisis de imagen de Amazon ha detectado.
    # La sintaxis de la respuesta que retorna se puede cosultar en la documentación
    # La información de los rostros está en el objeto FaceDetails
    for faceDetail in response['FaceDetails']:
        # BoundingBox es el marco donde se detecta el rostro
        # faceDetail devuelve los detalles de los rostros
        box = faceDetail['BoundingBox']
        # Se obtienen los píxeles exactos donde está el rostro
        # Cada valor de BoundingBox será un porcentaje entre 0 y 1
        x = int(width * box['Left'])
        y = int(height * box['Top'])
        w = int(width * box['Width'])
        h = int(height * box['Height'])

        # Obtener todos los píxeles de la región de interés
        # desde la esquina superior izquierda a la esquina 
        # inferior derecha del cuadro delimitador.
        # Se recorre una matriz que define todos los píxeles
        roi = img[y:y+h, x:x+w]

        # Aplicar el filtro de difuminado gausiano sobre la región que contiene el rostro
        # Cuanto mayor sea los valores del segundo parámetro (matriz del área escaneada) mayor será el 
        # difuminado de la región. El tercer parámetro es la desviación estándar del eje X
        roi = cv2.GaussianBlur(roi, (83, 83), 30)

        # Copiar en la imagen original el resultado de los píxeles difuminados
        img[y:y+roi.shape[0], x:x+roi.shape[1]] = roi

    print("Blurred face task has been successfully run")
    
    # Codificar la imagen para convertirla de nuevo en un conjunto de bytes
    _, res_buffer = cv2.imencode('.jpg', img)
    return res_buffer