FROM python:3.11-slim

WORKDIR /servidor

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /servidor/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
