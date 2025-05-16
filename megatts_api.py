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
    latent = data.get("latent")  # Ex: assets/English_prompt.npy

    if not text or not latent:
        return JSONResponse(
            {"error": "Envie 'text' e 'latent' (.npy)"},
            status_code=400
        )

    out_dir = "gen"
    os.makedirs(out_dir, exist_ok=True)

    output_path = os.path.join(out_dir, f"{uuid.uuid4()}.wav")

    command = [
        "python",
        "inference/synthesize_latent.py",
        "--config", "configs/ar-mel/finetune.yaml",
        "--text", text,
        "--latent_path", latent,
        "--output_path", output_path
    ]

    env = os.environ.copy()
    env["PYTHONPATH"] = "/app"

    try:
        subprocess.run(command, check=True, env=env, shell=False)

        if not os.path.exists(output_path):
            return JSONResponse(
                {"error": "Geração concluída mas o arquivo .wav não foi encontrado."},
                status_code=500
            )

        return FileResponse(output_path, media_type="audio/wav")

    except subprocess.CalledProcessError as e:
        return JSONResponse(
            {"error": f"Falha ao gerar áudio: {e}"},
            status_code=500
        )
