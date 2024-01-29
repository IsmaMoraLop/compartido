## INSTRUCCIONES PARA LA EJECUCIÓN DEL CASO PRÁCTICO

## IMPORTANTE: LAS INSTRUCCIONES DEBEN IR EN ESTE ORDEN Y EN NINGÚN OTRO

## ALGUNOS PASOS YA LOS DEBES TENER HECHOS DE PRÁCTICAS ANTERIORES
## SIN EMBARGO ASEGÚRATE QUE ESTÁ TODO LO NECESARIO INSTALADO

1. Abrir un terminal (1) en Ubuntu. Acceder como superusuario. Asegúrate que estas en el home de tu usuario (por ejemplo el mío es /home/garciameg#. Actualizar el sistema e instalar pip3. Comprueba que se ha instalado

#sudo su

#apt update

#apt upgrade

#apt-get install python3-pip

#pip --version

Ve limpiando la consola con 

#clear

2. INSTALAR el entorno virtual y comprobar que se ha instalado

#pip3 install virtualenv 

#virtualenv --version

3. En el directorio Documentos CREAR el entorno virtual de nombre blur-faces para independizar el contenido del proyecto (aislar recursos como bibliotecas, entornos de ejecución del sistema, etc. Se podrán tener varias versiones de una misma biblioteca sin crear conflictos entre ellas)

#python3 -m virtualenv blur-faces

4. Accede al entorno virtual que acabas de crear para ACTIVARLO. 

#cd blur-faces

#source bin/activate

5. INSTALAR los paquetes necesarios para desarrollar el sistema. Una vez instalados asegúrate que realmente se han instalado con el comando

#pip show nombre_paquete

## Acceder a servicios de Amazon 
#pip3 install boto3

## Framework
#pip3 install flask

## Cargar variables de entorno
#pip3 install python-dotenv

## Permitir la manipulación de imágenes, en concreto para pixelar los rostros de personas
#pip3 install opencv-Python

## Paquete usado en ciencia de datos para trabajar con matrices y funciones matemáticas
#pip3 install numpy

## Crear archivos de configuración
8. Instalar curl (SE NECESITARÁ MÁS ADELANTE PARA TRANSFERENCIA DE ARCHIVOS)
#apt install curl

6. Abrir y configurar el fichero .env con tus claves AWS y tus buckets

7. Crear y configurar los nodos de almacenamiento origen y destino 

#aws s3 mb s3://blur-source-bucket --region eu-west-2

#aws s3 mb s3://blur-dest-bucket --region eu-west-2

8. Subir alguna de las imágenes de la carpeta /imgs al S3 de origen.

#aws s3 cp imgs/nombre_imagen.jpg s3://blur-source-bucket --region eu-west-2

9. Ejecutar el servidor 
#python3 application.py

10. Abrir un segundo teminal (2) Ctrl + Alt + T

#curl -H "Content-Type: application/json" -X POST -d '{"key": "nombre_imagen.jpg"}' localhost:5000/api/analyze

11. Acceder a AWS desde la consola Web y comprobar que todo se ha realizado correctamente