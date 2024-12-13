FROM ghcr.io/withlogicco/poetry:1.7.0-python-3.12
WORKDIR /app
COPY pyproject.toml ./
RUN poetry install --no-root
COPY app app
COPY .env .env
COPY README.md README.md
ENV PYTHONPATH=/app
