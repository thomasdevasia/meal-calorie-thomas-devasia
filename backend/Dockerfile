FROM python:3.13-slim
WORKDIR /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
# CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
