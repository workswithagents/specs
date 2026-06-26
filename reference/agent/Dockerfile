FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn pydantic cryptography httpx

COPY main.py /app/

EXPOSE 8787
VOLUME ["/data"]
CMD ["python", "main.py"]
