FROM python:3.10.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y wget

RUN wget -O /app/service-account-key.json $(SECRET_URL)

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN pip install onnxruntime

COPY . .

# Set environment variable for Google Cloud credentials
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/service-account-key.json

EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]

