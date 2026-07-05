FROM python:3.14-slim

WORKDIR /app

# Системные зависимости для asyncpg
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Копируем зависимости
COPY pyproject.toml uv.lock ./

# Устанавливаем Python-зависимости
RUN uv sync --frozen

# Копируем код
COPY . .

# Активируем виртуальное окружение
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Запускаем миграции и сервер
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]