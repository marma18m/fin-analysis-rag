FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git && \
    pip install --upgrade pip

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Create working directory
WORKDIR /app

# Copia archivos del proyecto
COPY pyproject.toml poetry.lock* ./
COPY app/ app/
COPY qdrant_data/ qdrant_data/         
COPY .env .env                         

# Install dependencies
RUN poetry install --only main

# Expose the API port
EXPOSE 8000

# Start command
CMD ["poetry", "run", "uvicorn", "app.rag_api:app", "--host", "0.0.0.0", "--port", "8000"]

# build command
# docker build -t rag-api .

# execute command
# docker run -d -p 8000:8000 --name rag-api-container rag-api