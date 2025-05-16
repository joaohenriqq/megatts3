FROM python:3.11-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y git ffmpeg && apt-get clean

# Cria diretório de trabalho
WORKDIR /app

# Clona o MegaTTS3
RUN git clone https://github.com/bytedance/MegaTTS3.git . && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install fastapi uvicorn

# Copia o script de API
COPY megatts_api.py /app/megatts_api.py

# Porta padrão
EXPOSE 7860

# Define o path da aplicação para que o Python encontre os módulos
ENV PYTHONPATH=/app

# Inicia a API
CMD ["uvicorn", "megatts_api:app", "--host", "0.0.0.0", "--port", "7860"]
