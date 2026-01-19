FROM python:3.10.10-slim-bookworm

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt перед всеми файлами для кэширования слоёв
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY . .

# приложение слушает на всех интерфейсах (0.0.0.0), а не только localhost
EXPOSE 5000

# Запускаем приложение
CMD ["python", "app.py"]