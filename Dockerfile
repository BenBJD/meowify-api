FROM nvidia/cuda:12.9.0-runtime-ubuntu24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy the project files
COPY pyproject.toml uv.lock /app/
COPY api/ /app/api/

# Install dependencies using uv
RUN uv sync --python 3.11

ENV PATH="/app/.venv/bin:$PATH"

# Expose the API port
EXPOSE 8000

# Leaving with this for now
CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000"]