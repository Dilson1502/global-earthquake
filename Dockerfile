FROM python:3.9-slim

WORKDIR /app

COPY requirements-devel.txt .

RUN pip install --no-cache-dir -r requirements-devel.txt

COPY . .

EXPOSE 5005

CMD CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "5005", "--reload"]
