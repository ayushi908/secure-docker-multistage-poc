# -------- Stage 1: Base --------
FROM python:3.11-slim AS base

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# -------- Stage 2: Builder --------
FROM base AS builder

# Copy application code
COPY app/ /app

# -------- Stage 3: Runtime --------
FROM python:3.11-slim AS runtime

# Create non-root user
RUN useradd -u 1000 -m appuser

WORKDIR /app

# Copy only required files from builder
COPY --from=builder /app /app

# Set proper ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

EXPOSE 5000

# Optional healthcheck (strong addition)
#HEALTHCHECK CMD curl --fail http://localhost:5000/health || exit 1

CMD ["python", "app.py"]