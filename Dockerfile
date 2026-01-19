FROM python:3.10.10-slim-bookworm
WORKDIR /app
COPY . .
ENTRYPOINT ["python", "app.py"]