# syntax=docker/dockerfile:1.2

FROM python:3.9-slim-buster as python
FROM python as python-build-stage

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    # psycopg2
    libpq-dev \
    build-essential

COPY ./requirements.txt .

RUN pip wheel \
    --wheel-dir /usr/src/app/wheels \
    -r requirements.txt

FROM python as python-run-stage

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN pip install --upgrade pip

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    build-essential \
    # translations
    gettext \
    # cleaning up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=python-build-stage /usr/src/app/wheels /wheels

RUN pip install --no-cache-dir --no-index \
    --find-links=/wheels /wheels/* \
    && rm -rf /wheels

RUN echo 'export PS1="🐳 \[\033[1;36m\]/\W\[\033[0;35m\] \[\033[0m\]"' >> ~/.bashrc

COPY ./docker/entrypoint /entrypoint
COPY ./docker/start /start

COPY . .

ENTRYPOINT ["/entrypoint"]
CMD ["/start"]
