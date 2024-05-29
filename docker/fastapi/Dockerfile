FROM python:3.11-bullseye
WORKDIR /app
COPY requirements.txt server/
COPY pyproject.toml .
RUN pip install --no-cache-dir -r server/requirements.txt
COPY server/ server/
COPY tests/ tests/
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]