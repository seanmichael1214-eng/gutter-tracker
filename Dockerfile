FROM python:3.11-slim-bullseye
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY requirements.txt requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY . .
# Production-ready Gunicorn server
EXPOSE 5000
CMD ["gunicorn", "run:app", "-b", "0.0.0.0:5000", "--workers", "2", "--log-level", "info"]
