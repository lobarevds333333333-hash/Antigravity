FROM python:3.11-slim

WORKDIR /app

# Сначала ставим библиотеки (чтобы кешировались)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Потом копируем ВЕСЬ проект (main.py и всё остальное) в папку /app
COPY . .

# Запускаем!
CMD ["python", "main.py"]
