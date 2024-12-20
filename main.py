import uvicorn
from fastapi import FastAPI, File, UploadFile
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pathlib
import shutil
from ollama import generate


load_dotenv()

app = FastAPI(title="Ollama Web Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = pathlib.Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/favicon.ico")
async def read_favicon():
    return {}


@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...)):
    os.makedirs("audio", exist_ok=True)
    file_path = f"audio/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"info": f"File uploaded to {file_path}"}


@app.get("/")
async def read_index():
    return FileResponse(static_dir / "index.html")


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="localhost",
        port=8000,
        log_level="debug",
        ssl_keyfile="cert/key.key",
        ssl_certfile="cert/cert.crt",
    )  # TODO remove debug mode
