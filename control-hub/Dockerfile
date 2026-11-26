FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN useradd --create-home --uid 10001 runner
WORKDIR /workspace
USER runner
CMD ["python", "-m", "compileall", "-q", "backend"]
