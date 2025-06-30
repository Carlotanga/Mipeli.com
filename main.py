from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from client import crear_cliente_r2
from io import BytesIO
import boto3
from fastapi import Header

app = FastAPI()

# Configuración R2
r2 = crear_cliente_r2()
BUCKET_NAME = "mipeli-videos"
BASE_URL = "https://4290f283a95f956d408d2fb126d0f952.r2.cloudflarestorage.com/mipeli-videos"

# Templates
templates = Jinja2Templates(directory="templates")

# 🟢 Subir archivos al bucket
@app.post("/subir/{pelicula}/")
async def subir_video(pelicula: str, file: UploadFile = File(...)):
    pelicula = pelicula.lower()
    ruta_remota = f"{pelicula}/{file.filename}"
    r2.upload_fileobj(file.file, BUCKET_NAME, ruta_remota)
    url_publica = f"{BASE_URL}/{ruta_remota}"
    return {"url": url_publica}

# 🟢 Ver película (página HTML dinámica)
@app.get("/ver/{pelicula}", response_class=HTMLResponse)
async def ver_pelicula(pelicula: str, request: Request):
    pelicula = pelicula.lower()
    manifest_url = f"/stream/{pelicula}/manifest.mpd"  # se usa proxy local
    return templates.TemplateResponse("ver.html", {
        "request": request,
        "manifest_url": manifest_url,
        "titulo": pelicula.capitalize()
    })

# 🟢 Proxy local para evitar CORS con R2
@app.get("/stream/{pelicula}/{archivo}")
async def proxy_archivo(pelicula: str, archivo: str, range: str = Header(None)):
    key = f"{pelicula}/{archivo}"
    try:
        # Construir argumentos para el get_object con rango si existe
        get_obj_args = {"Bucket": BUCKET_NAME, "Key": key}
        if range:
            get_obj_args["Range"] = range

        objeto = r2.get_object(**get_obj_args)
        body = objeto['Body'].read()
        content_type = objeto.get('ContentType', "application/octet-stream")
        status_code = 206 if range else 200  # 206 Partial Content si es con rango

        return StreamingResponse(BytesIO(body), media_type=content_type, status_code=status_code)
    except r2.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))