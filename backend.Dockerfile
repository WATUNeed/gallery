FROM python:3.11-slim-buster

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt clean && \
    rm -rf /var/cache/apt/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

COPY requirements/ /tmp/requirements/

RUN pip install -U pip &&  \
    pip install --no-cache-dir -r /tmp/requirements/backend.txt

COPY backend/ /src/backend/

# COPY app/run_consume.py /src/run_consume.py

WORKDIR /src/

# CMD ["/bin/bash", "-c", "source uvicorn backend.main:app --host 0.0.0.0 --port 8000"]
# CMD ["/bin/bash", "-c", "source /src/venv/bin/activate && pytest -s -vv backend/tests/* -W ignore::DeprecationWarning && uvicorn backend.main:app --host 0.0.0.0 --port 8000"]