FROM python:3.9-slim

WORKDIR /app

COPY requirements-devel.txt .

RUN pip install --no-cache-dir -r requirements-devel.txt

WORKDIR /app

EXPOSE 5005

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "5005"]