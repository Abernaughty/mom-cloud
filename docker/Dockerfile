# mom-cloud pipeline container
#
# TODO: Implement in M4 (Issue #4)

FROM python:3.11-slim AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

ENTRYPOINT ["python", "-m", "src.ingest"]
