import os
from client import crear_cliente_r2  # tu cliente configurado
import mimetypes

r2 = crear_cliente_r2()
BUCKET_NAME = "mipeli-videos"
PELICULA = "mrbeast"  # nombre de la carpeta/pelicula en minúsculas
CARPETA_LOCAL = "./mrbeast_archivos"  # ruta local donde tienes los archivos segmentados

def subir_archivos_carpeta(local_folder, pelicula):
    for root, dirs, files in os.walk(local_folder):
        for file in files:
            local_path = os.path.join(root, file)
            # ruta remota dentro del bucket, manteniendo subcarpetas si las hay
            relative_path = os.path.relpath(local_path, local_folder)
            key = f"{pelicula}/{relative_path.replace(os.sep, '/')}"  # clave S3 con "/" para carpetas

            content_type, _ = mimetypes.guess_type(local_path)
            extra_args = {"ContentType": content_type} if content_type else {}

            with open(local_path, "rb") as f:
                print(f"Subiendo {local_path} a {key}")
                r2.upload_fileobj(f, BUCKET_NAME, key, ExtraArgs=extra_args)

if __name__ == "__main__":
    subir_archivos_carpeta(CARPETA_LOCAL, PELICULA)
