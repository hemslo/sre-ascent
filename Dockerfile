FROM python:3.11-slim as builder
RUN pip install poetry==1.7.1
RUN poetry config virtualenvs.in-project true
WORKDIR /code
COPY ./pyproject.toml ./README.md ./poetry.lock* ./
RUN poetry install --no-interaction --no-ansi --no-root --only main

FROM python:3.11-slim
WORKDIR /code
COPY ./app ./app
COPY --from=builder /code/.venv /code/.venv
EXPOSE 8000
ENV VIRTUAL_ENV=/code/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
CMD exec uvicorn app.server:app --host 0.0.0.0 --port 8000
