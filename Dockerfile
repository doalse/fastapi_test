# 1. Використаємо офіційний образ Python
FROM python:3.11-slim

# 2. Встановимо залежності
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Скопіюємо код у контейнер
COPY ./app ./app

# 4. Запуск FastAPI через uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]