FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN useradd --create-home --uid 10001 runner
WORKDIR /workspace
USER runner
CMD ["python", "-c", "import ast,pathlib; files=list(pathlib.Path('backend').rglob('*.py')); [ast.parse(p.read_text(encoding='utf-8'), filename=str(p)) for p in files]; print(f'Parsed {len(files)} backend Python files')"]
