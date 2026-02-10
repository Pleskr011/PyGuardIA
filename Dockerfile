# Usamos una imagen ligera de Python
FROM python:3.11.14-slim-bookworm

# Crear un usuario no privilegiado por seguridad
RUN useradd -m devsecuser
USER devsecuser
WORKDIR /home/devsecuser/app

# Copiar solo lo necesario
COPY --chown=devsecuser:devsecuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=devsecuser:devsecuser src/ ./src/

# Variables de entorno por defecto
ENV SCAN_PATH="./src"
ENV AI_PLATFORM="gemini"
ENV AI_API_KEY=""
ENV GITHUB_STEP_SUMMARY=""

# Ejecutar el scanner al iniciar
CMD ["sh", "-c", "python src/scanner.py --path $SCAN_PATH --ai_platform $AI_PLATFORM"]