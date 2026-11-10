# Image that builds the `calendar_scripts` Python library into a wheel.
#
# Multi-stage build:
#   1) builder — installs the build tools and produces the `.whl` in `/dist`.
#   2) runtime — slim image where the ready wheel is installed.
#
# Build the image:
#   docker build -t calendar-scripts:latest .
#
# Copy the built wheel out (without starting a container):
#   docker create --name cs calendar-scripts:latest
#   docker cp cs:/dist/. ./dist/
#   docker rm cs

# ── Stage 1: build the wheel ──────────────────────────────────────────────
FROM python:3.12-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /src

# Only the build files first, so the build-tools layer stays cached while the
# sources change.
COPY pyproject.toml README.md ./
RUN python -m pip install --upgrade pip build

# Package sources.
COPY calendar_scripts ./calendar_scripts

# Build the wheel into /dist.
RUN python -m build --wheel --outdir /dist

# ── Stage 2: image with the library installed ─────────────────────────────
FROM python:3.12-slim AS runtime

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# The built wheel is available for copying out.
COPY --from=builder /dist /dist

# Install the built library (with its dependencies).
RUN python -m pip install /dist/*.whl

# Fail the build if the package cannot be imported.
RUN python -c "import calendar_scripts; print('calendar_scripts OK')"

# Interactive shell by default: this is a library image, not a service.
CMD ["python"]
