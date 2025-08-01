FROM python:3.11-slim

WORKDIR /code
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install the application dependencies.
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-cache

# Copy the application into the container.
COPY . .
#
#RUN groupadd -r nonroot && useradd -r -g nonroot nonroot
#USER nonroot

CMD ["/code/.venv/bin/uvicorn", "src.main:fastfitapi", "--host", "0.0.0.0", "--port", "8000"]