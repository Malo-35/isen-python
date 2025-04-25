# Étape 1 : Construire l'environnement virtuel avec toutes les dépendances
FROM debian:12-slim AS build 

RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes \
        python3-venv=3.11.2-1+b1 \
        gcc=4:12.2.0-14 \
        libpython3-dev=3.11.2-1 && \
    python3 -m venv /venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt /requirements.txt

RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

# Étape 2 : Image finale ultra-légère
FROM gcr.io/distroless/python3-debian12:latest-amd64

COPY --from=build /venv /venv

WORKDIR /app
COPY . .

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
