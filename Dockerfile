# Этап 1: Сборка и компиляция C-зависимостей библиотек Python 
FROM python:3.9-slim AS builder
WORKDIR /app
# Установка gcc и build-essential для успешной компиляции расширений psutil
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
# Создание файла зависимостей
RUN echo "flask\npsutil==5.9.5" > requirements.txt
# Локальная изолированная установка зависимостей в каталог пользователя
RUN pip install --no-cache-dir --user -r requirements.txt
# Этап 2: Финальный продакшн образ
FROM python:3.9-slim
WORKDIR /app
# Перенос скомпилированных и чистых библиотек из слоя builder
COPY --from=builder /root/.local /root/.local
COPY app.py /app/
# Регистрация путей виртуального окружения в PATH контейнера
ENV PATH=/root/.local/bin:$PATH
# Перевод на порт 8888 в соответствии с ТЗ контрольной работы
EXPOSE 8888
ENTRYPOINT ["python", "app.py"]

