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
import whisper

load_dotenv()
AUDIO_RECORDING_PATH = "audio/recording.txt"

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
    with open(AUDIO_RECORDING_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    model = whisper.load_model("turbo")
    result = model.transcribe(AUDIO_RECORDING_PATH)
    with open(AUDIO_RECORDING_PATH, "w") as file:
        file.write(result["text"])
    return {"text": "Uploaded and transcribed audio"}


@app.get("/get_audio_text")
async def get_audio_text():
    if not os.path.exists(AUDIO_RECORDING_PATH):
        return {"text": ""}
    with open(AUDIO_RECORDING_PATH, "r") as file:
        text = file.read()
    return {"text": text}


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
