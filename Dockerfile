FROM python:3.9-slim-buster
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml /app
COPY poetry.lock /app
RUN poetry config virtualenvs.create false \
    && poetry config experimental.new-installer false \
    && poetry install --no-root --no-interaction --no-ansi \
    && pip cache purge
COPY . /app
EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
