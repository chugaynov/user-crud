# Базовый образ Alpine Linux с Python 3.12
FROM python:3.12-alpine

# Установка переменных окружения
ENV APP_PATH=/project \
    PYTHONPATH=/project/src \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Создание рабочей директории
WORKDIR $APP_PATH

# Установка зависимостей системы
RUN apk update && apk add --no-cache gcc musl-dev linux-headers

# Копирование файлов Poetry
COPY pyproject.toml poetry.lock* ./

# Установка Poetry и зависимостей
RUN pip install --no-cache-dir poetry==1.7.0 \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-dev

# Копирование исходного кода
COPY . .

# Смена пользователя
RUN adduser -u 101 -D python-user
USER python-user

# Порт приложения
EXPOSE 8080

# Команда запуска приложения
CMD ["python", "src/app/main.py"]