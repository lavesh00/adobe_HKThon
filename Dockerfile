# Dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY . .

# Install Python dependencies and spaCy model
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt \
    --default-timeout=120 --retries=5 && \
    python -m spacy download en_core_web_sm

# Preload the HuggingFace model so it's cached in the Docker image
RUN python preload_model.py

# Default command — accepts all arguments from Docker CLI
ENTRYPOINT ["python", "run.py"]
