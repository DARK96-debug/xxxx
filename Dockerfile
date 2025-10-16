# Python image
FROM python:3.11-slim

# Ishchi papka
WORKDIR /app

# Fayllarni konteynerga nusxalash
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Botni ishga tushirish
CMD ["python", "bot.py"]
