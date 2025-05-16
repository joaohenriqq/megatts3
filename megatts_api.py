from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
import uuid
import os
from tts.infer_cli import infer  # usa o script oficial

app = FastAPI()

@app.post("/synthesize")
async def synthesize(request: Request):
    data = await request.json()
    text = data.get("text")
    wav = data.get("wav")  # caminho de entrada .wav de referência
    if not text or not wav:
        return JSONResponse({"error": "Envie 'text' e 'wav'"}, status_code=400)

    out_dir = "/app/gen"
    os.makedirs(out_dir, exist_ok=True)

    output_path = os.path.join(out_dir, f"{uuid.uuid4()}.wav")

    infer(input_text=text, input_wav=wav, output_dir=out_dir)

    return FileResponse(output_path, media_type="audio/wav")
