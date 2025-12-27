FROM python:3.11-slim-bullseye
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY requirements.txt requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY . .
# Production-ready Gunicorn server (using PORT from environment, defaulting to 8080)
EXPOSE 8080
CMD ["sh", "-c", "gunicorn run:app -b 0.0.0.0:${PORT:-8080} --workers 1 --threads 2 --log-level info"]
