# ====== Python bazasi ======
FROM python:3.11-slim

# Ishchi papkani o‘rnatamiz
WORKDIR /app

# Fayllarni konteynerga nusxalash
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Bot faylini nusxalash
COPY bot.py .

# Aplarni avtomatik ishga tushirish
CMD ["python", "bot.py"]
