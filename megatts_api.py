from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
import uuid
import os
import subprocess

app = FastAPI()

@app.post("/synthesize")
async def synthesize(request: Request):
    data = await request.json()
    text = data.get("text")
    wav = data.get("wav")  # caminho do áudio de referência .wav

    if not text or not wav:
        return JSONResponse({"error": "Envie 'text' e 'wav'"}, status_code=400)

    out_dir = "/app/gen"
    os.makedirs(out_dir, exist_ok=True)
    output_path = os.path.join(out_dir, f"{uuid.uuid4()}.wav")

    command = [
        "python", "tts/infer_cli.py",
        "--input_wav", wav,
        "--input_text", text,
        "--output_dir", out_dir
    ]

    try:
        subprocess.run(command, check=True)
        return FileResponse(output_path, media_type="audio/wav")
    except subprocess.CalledProcessError as e:
        return JSONResponse({"error": f"Falha ao gerar áudio: {e}"}, status_code=500)
