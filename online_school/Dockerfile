# Часть1. Подготовка зависимостей к использованию в приложении
FROM python:3.10-alpine as builder

# Установить рабочую директорию внутри контейнера (любое название)
# все последующие команды будут выполняться в этой директории
WORKDIR /online_school_web 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Скопировать зависимости проекта в контейнер
COPY ./requirements.txt .

# Установить зависимости проекта
# RUN pip install -r requirements.txt

# Создать архивы Python-пакетов. Они содержат скомпилированный код, что ускоряет установку пакетов
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /online_school_web/wheels -r requirements.txt

#RUN apt-get update && apt install -y netcat-openbsd
RUN apk update && apk add --no-cache netcat-openbsd

#============================================================
# Часть2. Создание финального образа Docker, который содержит только то, что нужно для работы приложения.
FROM python:3.10-alpine
RUN pip install gunicorn

# create directory for the app user
RUN mkdir -p /home/online_school_web

# create the app user
RUN addgroup -S online_school_web && adduser -S online_school_web -G online_school_web

# домашний каталог пользователя внутри контейнера
ENV HOME=/home/online_school_web
# а здесь будет располагаться само приложение внутри контейнера.
ENV APP_HOME=/home/online_school_web/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /online_school_web/wheels /wheels
COPY --from=builder /online_school_web/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' $APP_HOME/entrypoint.sh
RUN chmod +x $APP_HOME/entrypoint.sh

# Скопировать все содержимое текущей директории в контейнер
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R online_school_web:online_school_web $APP_HOME

# change to the app user
USER online_school_web

# Команда запуска приложения
# CMD ["python3", "online_school/manage.py", "runserver", "0.0.0.0:8000"]
# run entrypoint.sh
ENTRYPOINT ["/home/online_school_web/web/entrypoint.sh"]