FROM python:3.11-bullseye
WORKDIR /server
COPY requirements.txt /server/
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY docker/fastapi/local_run.sh /server/docker/fastapi/local_run.sh
RUN chmod +x /server/docker/fastapi/local_run.sh
CMD ["uvicorn", "main:server", "--host", "0.0.0.0", "--port", "8000"]