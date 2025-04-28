# Étape 1 : Build
FROM python:3.9-slim-buster as build

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes \
        python3-venv \
        gcc \
        libpython3-dev && \
    python3 -m venv /venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt

RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

# Étape 2 : Image finale
FROM gcr.io/distroless/python3-debian12:latest-amd64

COPY --from=build /venv /venv

WORKDIR /app
COPY . .

EXPOSE 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
