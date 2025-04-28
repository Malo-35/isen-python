FROM python:3.9-slim-buster

COPY requirements.txt /requirements.txt

RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

# Étape 2 : Image finale ultra-légère
FROM gcr.io/distroless/python3-debian12:latest-amd64

COPY --from=build /venv /venv

WORKDIR /app
COPY . .

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]