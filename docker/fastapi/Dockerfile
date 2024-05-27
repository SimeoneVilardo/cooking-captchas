FROM python:3.11-bullseye
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY server/. /app
COPY docker/fastapi/local_run.sh /app/docker/fastapi/local_run.sh
RUN chmod +x /app/docker/fastapi/local_run.sh
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]