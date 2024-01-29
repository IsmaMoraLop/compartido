# Código que implementa el comportamiento inteligente de la aplicación

# Para acceso a variables de entorno guardadas en el archivo .env
import os
# Implementación de Amazon para acceder a sus servicios
import boto3
# Para cargar las variables de entorno del archivo .env
from dotenv import load_dotenv

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Obtener las variables de entorno
accessKeyId = os.environ.get('ACCESS_KEY_ID')
secretKey = os.environ.get('ACCESS_SECRET_KEY')
bucket = os.environ.get('BUCKET_SOURCE')
region = os.environ.get('REGION')

# Crear sesión de Amazon para el servicio Rekognition y asignar credenciales
# Si la sesión expira, se reanudará cuando se realice una nueva llamada al servicio
rekognition_client = boto3.Session(
    aws_access_key_id=accessKeyId,
    aws_secret_access_key=secretKey,
    region_name=region).client('rekognition')

# Función que implementa el funcionamiento inteligente
# img: nombre de la imagen alojada en el nodo de almacenamiento origen
def detect_faces(img):
    # Asignar parámetros y llamada al servicio
    try:
        # Llamar al servicio de reconocimiento facial de Amazon, 
        # pasando el nombre del nodo de origen y la imagen a analizar
        # Se indica que en la respuesta se reciban los atributos por defecto
        response = rekognition_client.detect_faces(
            Image={'S3Object': {'Bucket': bucket, 'Name': img}}, Attributes=['DEFAULT'])

        print("Image task recognition has been successfully run")
    except:
        raise Exception("An unexpected error was raised recognizing an image")
    # Devuelve el contenido que el análisis facial envía
    return response
