# Código del servidor

# Importar paquetes
import boto3, os, base64
from flask import Flask, request, Response, abort
from dotenv import load_dotenv
# Para detectar y anonimizar rostros
from detect_faces import detect_faces
from blur_faces import anonymize_face

# Cargar las variables de entorno del fichero .env
load_dotenv()

# Obtener las variables de entorno
accessKeyId = os.environ.get('ACCESS_KEY_ID')
secretKey = os.environ.get('ACCESS_SECRET_KEY')
bucket_source = os.environ.get('BUCKET_SOURCE')
bucket_dest = os.environ.get('BUCKET_DEST')

# Crear la aplicación Flask
application = Flask(__name__)

# Crear sesión para acceder al servicio Amazon S3 y asignar credenciales
# Para acceder al nodo de almacenamiento y recuperar la imagen
s3 = boto3.Session(
    aws_access_key_id=accessKeyId,
    aws_secret_access_key=secretKey).resource('s3')

# api/analyze endpoint accedido mediante método POST
@application.route('/api/analyze', methods=['POST'])
# Contiene la implementación para ejecutar el comportamiento inteligente
def analyzeImage():
    # Control de error por si el resultado de la petición no es el esperado
    key = request.get_json()['key']
    if key is None:
        abort(400)
    
    try:
        # Devuelve la respuesta de la petición de servicio de análisis de imagen
        response = detect_faces(key)

        # Acceder al nodo de almacenamiento y recuperar la imagen
        fileObject = s3.Object(bucket_source, key).get()
        fileContent = fileObject['Body'].read()
        # Parámetros de llamada a la función para anonimizar caras:
        # la imagen en bytes y la respuesta devuelta por el servicio
        # de Amazon de reconocimiento de imágenes
        buffer_anon_img = anonymize_face(fileContent, response)
        # Transformar la imagen comprimida en bytes para subir su 
        # contenido al nodo de almacenamiento destino
        img_enc = base64.b64encode(buffer_anon_img)
        img_dec = base64.b64decode(img_enc)
        s3.Object(bucket_dest, f"result_{key}").put(Body=img_dec)
    except Exception as error:
        print(error)
        abort(500)
    return Response(status=200)

# El servidor se ejecuta en el localhost en el puerto 5000 http://127.0.0.1:5000/
if __name__ == "__main__":
    application.debug = True
    application.run()  